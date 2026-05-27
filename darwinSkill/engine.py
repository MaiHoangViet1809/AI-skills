from __future__ import annotations

from dataclasses import asdict
from math import ceil
from pathlib import Path
from uuid import uuid4

from darwinSkill.contracts import (
    BatchSpec,
    CandidateSkill,
    ComparisonPair,
    EvaluationReport,
    GateDecision,
    MetaSkillRecord,
    PatchGroup,
    RunContext,
    SelectionDecision,
    SkillFeedback,
    SkillPatch,
    SkillSample,
    SlowUpdateRecord,
    TrainingConfig,
)
from darwinSkill.runtime import build_feedback, build_report
from darwinSkill.storage import (
    build_run_state,
    ensure_output_dir,
    load_run_state,
    persist_best_skill,
    persist_epoch_payload,
    persist_skill_snapshot,
    persist_step_payload,
    isoformat,
    utc_now,
    write_json,
)


SLOW_UPDATE_START = "<!-- SLOW_UPDATE_START -->"
SLOW_UPDATE_END = "<!-- SLOW_UPDATE_END -->"


def _group_batches(samples: list[SkillSample], batch_size: int) -> list[list[SkillSample]]:
    return [
        samples[index : index + batch_size]
        for index in range(0, len(samples), batch_size)
    ] or [[]]


def build_batch_specs(samples: list[SkillSample], config: TrainingConfig) -> list[BatchSpec]:
    step = 0
    specs: list[BatchSpec] = []
    grouped = _group_batches(samples, config.batch_size)
    for epoch in range(1, config.num_epochs + 1):
        for batch in grouped:
            step += 1
            specs.append(BatchSpec(epoch=epoch, step=step, samples=list(batch)))
    return specs


def _build_rollout(context: RunContext, skill_text: str, samples: list[SkillSample]) -> EvaluationReport:
    predictions = [context.backend.predict(skill_text, sample) for sample in samples]
    evaluations = []
    for sample, prediction in zip(samples, predictions):
        metric = context.evaluator.evaluate(prediction, sample)
        from darwinSkill.contracts import SampleEvaluation

        evaluations.append(
            SampleEvaluation(
                sample=sample,
                prediction=prediction,
                metric=metric,
            )
        )
    return build_report(skill_text=skill_text, evaluations=evaluations)


def reflect_patches(
    report: EvaluationReport,
    *,
    meta_skill: str = "",
    slow_update_guidance: str = "",
) -> list[SkillPatch]:
    patches: list[SkillPatch] = []
    for index, item in enumerate(report.results, start=1):
        if item.metric.passed:
            continue
        guidance = []
        if meta_skill:
            guidance.append("meta_skill")
        if slow_update_guidance:
            guidance.append("slow_update")
        patches.append(
            SkillPatch(
                patch_id=f"patch-{index}-{uuid4().hex[:8]}",
                sample=item.sample,
                prediction=item.prediction,
                metric=item.metric,
                instruction=f"remember exact answer for: {item.sample.prompt}",
                support_count=1,
                metadata={
                    "expected_answer": item.sample.expected_answer,
                    "guidance_sources": guidance,
                },
            )
        )
    return patches


def aggregate_patches(patches: list[SkillPatch]) -> list[PatchGroup]:
    grouped: dict[str, list[SkillPatch]] = {}
    for patch in patches:
        key = patch.sample.prompt.strip()
        grouped.setdefault(key, []).append(patch)
    groups: list[PatchGroup] = []
    for prompt, members in grouped.items():
        groups.append(
            PatchGroup(
                group_id=f"group-{uuid4().hex[:8]}",
                instruction=f"remember exact answer for: {prompt}",
                patches=members,
                support_count=sum(patch.support_count for patch in members),
                metadata={"prompt": prompt},
            )
        )
    groups.sort(key=lambda item: (-item.support_count, item.metadata.get("prompt", "")))
    return groups


def select_patch_groups(groups: list[PatchGroup], edit_budget: int) -> SelectionDecision:
    selected_groups = list(groups[:edit_budget])
    selected_patches = [patch for group in selected_groups for patch in group.patches]
    return SelectionDecision(
        selected_groups=selected_groups,
        selected_patches=selected_patches,
        edit_budget=edit_budget,
        total_candidates=len(groups),
    )


def update_skill_text(
    context: RunContext,
    current_skill: str,
    selection: SelectionDecision,
) -> CandidateSkill:
    feedback: list[SkillFeedback] = [
        SkillFeedback(sample=patch.sample, prediction=patch.prediction, metric=patch.metric)
        for patch in selection.selected_patches
    ]
    candidate_text = context.backend.improve_skill(current_skill, feedback)
    return CandidateSkill(skill_text=candidate_text, selection=selection)


def gate_candidate(
    *,
    current_skill: str,
    current_report: EvaluationReport,
    best_skill: str,
    best_report: EvaluationReport,
    candidate: CandidateSkill,
) -> GateDecision:
    candidate_report = candidate.candidate_report
    if candidate_report is None:
        raise ValueError("Candidate report must be evaluated before gating.")
    if candidate_report.mean_score > current_report.mean_score:
        accepted_skill = candidate.skill_text
        accepted_report = candidate_report
        if candidate_report.mean_score > best_report.mean_score:
            return GateDecision(
                action="accept_new_best",
                accepted_skill=accepted_skill,
                accepted_report=accepted_report,
                best_skill=accepted_skill,
                best_report=accepted_report,
                candidate_skill=candidate.skill_text,
                candidate_report=candidate_report,
                previous_skill=current_skill,
                previous_report=current_report,
            )
        return GateDecision(
            action="accept",
            accepted_skill=accepted_skill,
            accepted_report=accepted_report,
            best_skill=best_skill,
            best_report=best_report,
            candidate_skill=candidate.skill_text,
            candidate_report=candidate_report,
            previous_skill=current_skill,
            previous_report=current_report,
        )
    return GateDecision(
        action="reject",
        accepted_skill=current_skill,
        accepted_report=current_report,
        best_skill=best_skill,
        best_report=best_report,
        candidate_skill=candidate.skill_text,
        candidate_report=candidate_report,
        previous_skill=current_skill,
        previous_report=current_report,
    )


def build_comparison_pairs(previous: EvaluationReport, current: EvaluationReport) -> list[ComparisonPair]:
    pairs: list[ComparisonPair] = []
    for previous_item, current_item in zip(previous.results, current.results):
        if previous_item.metric.passed and not current_item.metric.passed:
            category = "regressed"
        elif not previous_item.metric.passed and current_item.metric.passed:
            category = "improved"
        elif previous_item.metric.passed and current_item.metric.passed:
            category = "stable_success"
        else:
            category = "persistent_fail"
        pairs.append(
            ComparisonPair(
                sample=current_item.sample,
                previous_prediction=previous_item.prediction,
                current_prediction=current_item.prediction,
                previous_metric=previous_item.metric,
                current_metric=current_item.metric,
                category=category,
            )
        )
    return pairs


def _build_guidance_lines(pairs: list[ComparisonPair], *, include_improvements: bool) -> list[str]:
    lines: list[str] = []
    for pair in pairs:
        if pair.category == "regressed":
            lines.append(
                f"- do not forget: {pair.sample.prompt} => {pair.sample.expected_answer}"
            )
        elif pair.category == "persistent_fail":
            lines.append(
                f"- unresolved: {pair.sample.prompt} => {pair.sample.expected_answer}"
            )
        elif include_improvements and pair.category == "improved":
            lines.append(
                f"- keep improvement: {pair.sample.prompt} => {pair.sample.expected_answer}"
            )
    return lines


def build_slow_update_record(epoch: int, pairs: list[ComparisonPair]) -> SlowUpdateRecord:
    guidance_lines = _build_guidance_lines(pairs, include_improvements=True)
    guidance = "\n".join(guidance_lines).strip()
    return SlowUpdateRecord(epoch=epoch, guidance=guidance, comparisons=pairs)


def build_meta_skill_record(epoch: int, pairs: list[ComparisonPair], previous_meta: str) -> MetaSkillRecord:
    buckets = {
        "improved": sum(1 for pair in pairs if pair.category == "improved"),
        "regressed": sum(1 for pair in pairs if pair.category == "regressed"),
        "persistent_fail": sum(1 for pair in pairs if pair.category == "persistent_fail"),
        "stable_success": sum(1 for pair in pairs if pair.category == "stable_success"),
    }
    notes = [f"epoch={epoch}"]
    if previous_meta.strip():
        notes.append("previous_meta=present")
    for key, value in buckets.items():
        notes.append(f"{key}={value}")
    notes.extend(_build_guidance_lines(pairs, include_improvements=False))
    return MetaSkillRecord(epoch=epoch, content="\n".join(notes).strip(), comparisons=pairs)


def inject_slow_update_guidance(skill_text: str, guidance: str) -> str:
    if not guidance.strip():
        return skill_text
    block = f"{SLOW_UPDATE_START}\n{guidance.strip()}\n{SLOW_UPDATE_END}"
    if SLOW_UPDATE_START in skill_text and SLOW_UPDATE_END in skill_text:
        start = skill_text.index(SLOW_UPDATE_START)
        end = skill_text.index(SLOW_UPDATE_END) + len(SLOW_UPDATE_END)
        return f"{skill_text[:start].rstrip()}\n{block}\n{skill_text[end:].lstrip()}".strip()
    if skill_text.strip():
        return f"{skill_text.rstrip()}\n\n{block}"
    return block


def _persist_runtime_state(context: RunContext) -> None:
    if context.output_dir is None:
        raise ValueError("RunContext.output_dir must exist before runtime-state persistence.")
    runtime_state = build_run_state(context, finished_at=isoformat(utc_now()))
    write_json(context.output_dir / "run_state.json", runtime_state)


class ReflectiveSkillEngine:
    def run_training(
        self,
        context: RunContext,
        *,
        config: TrainingConfig,
    ) -> RunContext:
        output_dir = (
            Path(config.resume_from)
            if config.resume_from is not None
            else ensure_output_dir(context.output_root, context.run_name, context.run_id)
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "steps").mkdir(exist_ok=True)
        (output_dir / "skills").mkdir(exist_ok=True)
        context.output_dir = output_dir

        train_samples = list(context.train_samples or context.samples)
        eval_samples = list(context.eval_samples or context.samples)
        batch_specs = build_batch_specs(train_samples, config)
        total_steps = len(batch_specs)
        full_current_report = _build_rollout(context, context.skill_text, eval_samples)

        current_skill = context.skill_text
        current_report = full_current_report
        best_skill = current_skill
        best_report = full_current_report
        context.current_report = current_report
        context.best_skill_text = best_skill
        context.best_report = best_report

        start_step = 0
        start_epoch = 1
        if config.resume_from is not None:
            resumed_state = load_run_state(Path(config.resume_from) / "run_state.json")
            current_skill = resumed_state.skill_text
            best_skill = resumed_state.best_skill_text
            start_step = resumed_state.current_step
            start_epoch = resumed_state.current_epoch
            current_report = _build_rollout(context, current_skill, eval_samples)
            best_report = _build_rollout(context, best_skill, eval_samples)
            context.started_at = resumed_state.started_at
            context.current_report = current_report
            context.best_report = best_report
            context.best_skill_text = best_skill
            context.best_step = resumed_state.best_step
            context.history.append({"stage": "resume", "from_step": start_step, "from_epoch": start_epoch})
        else:
            persist_skill_snapshot(output_dir, 0, current_skill)
            persist_best_skill(output_dir, best_skill)

        epoch_baseline = current_report
        for spec in batch_specs[start_step:]:
            context.current_epoch = spec.epoch
            context.current_step = spec.step

            if spec.step > 1 and spec.epoch != start_epoch and (spec.step - 1) % max(1, ceil(len(train_samples) / config.batch_size)) == 0:
                epoch_baseline = current_report

            batch_rollout = _build_rollout(context, current_skill, spec.samples)
            patches = reflect_patches(
                batch_rollout,
                meta_skill=context.meta_skill,
                slow_update_guidance=context.slow_update_guidance,
            )
            groups = aggregate_patches(patches)
            selection = select_patch_groups(groups, config.edit_budget)
            candidate = update_skill_text(context, current_skill, selection)
            candidate.candidate_report = _build_rollout(context, candidate.skill_text, eval_samples)
            gate = gate_candidate(
                current_skill=current_skill,
                current_report=current_report,
                best_skill=best_skill,
                best_report=best_report,
                candidate=candidate,
            )

            current_skill = gate.accepted_skill
            current_report = gate.accepted_report
            best_skill = gate.best_skill
            best_report = gate.best_report
            context.skill_text = current_skill
            context.current_report = current_report
            context.best_skill_text = best_skill
            context.best_report = best_report
            context.best_step = spec.step if gate.action == "accept_new_best" else context.best_step
            context.last_action = gate.action
            context.history.append(
                {
                    "stage": "gate",
                    "action": gate.action,
                    "epoch": spec.epoch,
                    "step": spec.step,
                    "current_score": current_report.mean_score,
                    "best_score": best_report.mean_score,
                }
            )

            skill_path = persist_skill_snapshot(output_dir, spec.step, current_skill)
            best_skill_path = persist_best_skill(output_dir, best_skill)
            step_record = {
                "epoch": spec.epoch,
                "step": spec.step,
                "batch_size": len(spec.samples),
                "rollout": asdict(batch_rollout),
                "patches": [asdict(patch) for patch in patches],
                "groups": [asdict(group) for group in groups],
                "selection": asdict(selection),
                "candidate_skill": candidate.skill_text,
                "candidate_report": asdict(candidate.candidate_report),
                "gate": asdict(gate),
                "current_skill_path": str(skill_path),
                "best_skill_path": str(best_skill_path),
            }
            context.step_records.append(step_record)
            persist_step_payload(output_dir, spec.step, "step_record.json", step_record)
            persist_step_payload(output_dir, spec.step, "candidate_skill.txt", candidate.skill_text)
            _persist_runtime_state(context)

            steps_per_epoch = max(1, ceil(len(train_samples) / config.batch_size))
            epoch_completed = spec.step % steps_per_epoch == 0
            if epoch_completed:
                comparisons = build_comparison_pairs(epoch_baseline, current_report)
                if config.use_slow_update:
                    slow_record = build_slow_update_record(spec.epoch, comparisons)
                    context.slow_update_guidance = slow_record.guidance
                    current_skill = inject_slow_update_guidance(current_skill, slow_record.guidance)
                    best_skill = inject_slow_update_guidance(best_skill, slow_record.guidance)
                    context.skill_text = current_skill
                    context.best_skill_text = best_skill
                    persist_epoch_payload(output_dir, "slow_update", spec.epoch, "slow_update.json", asdict(slow_record))
                if config.use_meta_skill:
                    meta_record = build_meta_skill_record(spec.epoch, comparisons, context.meta_skill)
                    context.meta_skill = meta_record.content
                    persist_epoch_payload(output_dir, "meta_skill", spec.epoch, "meta_skill.json", asdict(meta_record))
                persist_skill_snapshot(output_dir, spec.step, current_skill)
                persist_best_skill(output_dir, best_skill)
                current_report = _build_rollout(context, current_skill, eval_samples)
                context.current_report = current_report
                context.best_skill_text = best_skill
                context.best_report = best_report
                epoch_baseline = current_report
                _persist_runtime_state(context)

        final_report = _build_rollout(context, current_skill, eval_samples)
        context.skill_text = current_skill
        context.evaluation_report = final_report
        context.current_report = final_report
        context.best_skill_text = best_skill
        context.best_report = best_report
        return context
