from __future__ import annotations

from functools import partial
import importlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from darwinSkill.contracts import MetricResult, SkillEvaluator, SkillSample
from darwinSkill.reference_assets import REPO_ROOT, is_split_dir

ALFWORLD_TASKS = [
    "pick_and_place",
    "pick_two_obj_and_place",
    "look_at_obj_in_light",
    "pick_heat_then_place_in_recep",
    "pick_cool_then_place_in_recep",
    "pick_clean_then_place_in_recep",
]
ALFWORLD_SYSTEM_PROMPT = "You are an expert agent operating in the ALFRED Embodied Environment."


class ALFWorldAgentBackend(Protocol):
    def respond(
        self,
        *,
        system: str,
        user: str,
        messages: list[dict[str, Any]] | None = None,
    ) -> str | dict[str, Any]:
        ...


class ALFWorldEpisodeEnvironment(Protocol):
    def reset(self) -> dict[str, Any]:
        ...

    def step(self, action: str) -> dict[str, Any]:
        ...

    def close(self) -> None:
        ...


def _load_items(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Expected JSON array in {path}")
    return [dict(item) for item in payload]


def _resolve_data_file(path: Path) -> Path:
    if path.is_file():
        return path
    candidates = sorted(path.glob("*.json"))
    if len(candidates) != 1:
        raise ValueError(f"ALFWorld expects exactly one JSON file under {path}")
    return candidates[0]


def _infer_eval_dataset(gamefile: str) -> str:
    if "/valid_seen/" in gamefile:
        return "eval_in_distribution"
    if "/valid_unseen/" in gamefile:
        return "eval_out_of_distribution"
    return "train"


def _infer_task_type_from_gamefile(gamefile: str) -> str:
    for task in ALFWORLD_TASKS:
        if task in gamefile:
            return task
    return "alfworld"


def _extract_task_description(observation: str) -> str:
    anchor = str(observation or "")
    marker = "Your task is to: "
    if marker in anchor:
        return anchor.split(marker, 1)[1].strip()
    return anchor.strip()


def _ensure_skillopt_reference_importable() -> None:
    reference_root = str(REPO_ROOT / "references" / "SkillOpt")
    if reference_root not in sys.path:
        sys.path.insert(0, reference_root)


def build_live_alfworld_env_manager(
    *,
    env_num: int = 1,
    eval_dataset: str = "eval_out_of_distribution",
    seed: int = 42,
    is_train: bool = False,
    specific_gamefiles: list[str] | None = None,
) -> Any:
    _ensure_skillopt_reference_importable()
    try:
        from omegaconf import OmegaConf
    except ImportError as exc:  # pragma: no cover - optional dependency path
        raise RuntimeError("Live ALFWorld bridge requires `omegaconf` to be installed.") from exc

    try:
        build_envs = importlib.import_module("skillopt.envs.alfworld.vendor.alfworld_envs")
        projection_module = importlib.import_module("skillopt.envs.alfworld.vendor.alfworld_projection")
        env_manager_module = importlib.import_module("skillopt.envs.alfworld.vendor.env_manager")
    except ImportError as exc:  # pragma: no cover - optional dependency path
        raise RuntimeError(
            "Live ALFWorld bridge requires the reference SkillOpt vendor modules and their runtime dependencies."
        ) from exc

    vendor_dir = REPO_ROOT / "references" / "SkillOpt" / "skillopt" / "envs" / "alfworld" / "vendor"
    alf_config_path = vendor_dir / "config_tw.yaml"
    envs = build_envs.build_alfworld_envs(  # type: ignore[attr-defined]
        str(alf_config_path),
        seed=seed,
        env_num=env_num,
        group_n=1,
        is_train=is_train,
        env_kwargs={"eval_dataset": eval_dataset},
        resources_per_worker=None,
        gamefiles=specific_gamefiles,
    )
    config = OmegaConf.create(
        {
            "env": {
                "history_length": 2,
                "env_name": "alfworld/AlfredTWEnv",
            }
        }
    )
    projection_f = partial(projection_module.alfworld_projection)  # type: ignore[attr-defined]
    manager_class = env_manager_module.AlfWorldEnvironmentManager  # type: ignore[attr-defined]
    return manager_class(envs, projection_f, config)


@dataclass(slots=True)
class ALFWorldManagerEpisodeEnvironment:
    manager: Any

    def reset(self) -> dict[str, Any]:
        observations, infos = self.manager.reset({})
        info = infos[0] if infos else {}
        anchor = observations.get("anchor", [""])[0] if isinstance(observations, dict) else ""
        gamefile = str(info.get("extra.gamefile", "") or "")
        return {
            "observation": anchor,
            "gamefile": gamefile,
            "task_type": _infer_task_type_from_gamefile(gamefile),
            "task_description": _extract_task_description(anchor),
        }

    def step(self, action: str) -> dict[str, Any]:
        observations, rewards, dones, infos = self.manager.step([action])
        info = infos[0] if infos else {}
        anchor = observations.get("anchor", [""])[0] if isinstance(observations, dict) else ""
        return {
            "observation": anchor,
            "reward": float(rewards[0]) if rewards else 0.0,
            "done": bool(dones[0]) if dones else False,
            "won": bool(info.get("won", False)),
        }

    def close(self) -> None:
        close = getattr(self.manager, "close", None)
        if callable(close):
            close()


def build_live_alfworld_environment_factory(
    *,
    seed: int = 42,
    is_train: bool = False,
    env_manager_builder: Any | None = None,
) -> Any:
    builder = env_manager_builder or build_live_alfworld_env_manager

    def _factory(sample: SkillSample) -> ALFWorldManagerEpisodeEnvironment:
        metadata = sample.metadata
        gamefile = str(metadata.get("gamefile") or "").strip()
        if not gamefile:
            raise ValueError("ALFWorld live environment factory requires sample.metadata['gamefile'].")
        eval_dataset = str(metadata.get("eval_dataset") or _infer_eval_dataset(gamefile))
        manager = builder(
            env_num=1,
            eval_dataset=eval_dataset,
            seed=seed,
            is_train=is_train,
            specific_gamefiles=[gamefile],
        )
        return ALFWorldManagerEpisodeEnvironment(manager=manager)

    return _factory


def normalize_alfworld_record(record: dict[str, Any]) -> dict[str, Any]:
    gamefile = str(record.get("gamefile") or "").strip()
    task_description = str(record.get("task_description") or record.get("task_desc") or record.get("goal") or "").strip()
    task_type = str(record.get("task_type") or record.get("instruction_type") or "").strip() or _infer_task_type_from_gamefile(gamefile)
    result_id = str(record.get("id") or record.get("result_id") or gamefile or "env").strip()
    eval_dataset = str(record.get("eval_dataset") or _infer_eval_dataset(gamefile))
    return {
        "id": result_id,
        "gamefile": gamefile,
        "task_description": task_description or gamefile,
        "task_type": task_type,
        "instruction_type": task_type,
        "eval_dataset": eval_dataset,
        "expected_outcome": str(record.get("expected_outcome") or "success"),
        **{
            key: value
            for key, value in record.items()
            if key not in {"id", "result_id", "gamefile", "task_description", "task_desc", "goal", "task_type", "instruction_type", "eval_dataset", "expected_outcome"}
        },
    }


def load_alfworld_records(path: Path | str) -> list[dict[str, Any]]:
    data_path = Path(path)
    resolved = _resolve_data_file(data_path)
    return [normalize_alfworld_record(item) for item in _load_items(resolved)]


def load_alfworld_dataset(path: Path | str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = Path(path)
    if is_split_dir(root):
        train_records = load_alfworld_records(root / "train")
        eval_records = load_alfworld_records(root / "val")
        if not eval_records:
            eval_records = load_alfworld_records(root / "test")
        return train_records, eval_records or list(train_records)
    records = load_alfworld_records(root)
    return records, list(records)


def build_alfworld_samples(records: list[dict[str, Any]]) -> list[SkillSample]:
    return [
        SkillSample(
            prompt=str(normalize_alfworld_record(record).get("task_description", "")),
            expected_answer="success",
            metadata=normalize_alfworld_record(record),
        )
        for record in records
    ]


def extract_answer(text: str) -> str:
    matches = re.findall(r"<answer>(.*?)</answer>", text, re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[-1] if lines else text.strip()


def _load_prediction_payload(prediction: str) -> dict[str, Any] | None:
    stripped = prediction.strip()
    if not stripped or stripped[0] not in "{[":
        return None
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def extract_action(text: str) -> str | None:
    matches = re.findall(r"<action>(.*?)</action>", text, re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    return None


def extract_think(text: str) -> str | None:
    matches = re.findall(r"<think>(.*?)</think>", text, re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    return None


def build_alfworld_user_prompt(
    *,
    observation: str,
    skill_content: str = "",
    diagnostic_instruction: str = "",
) -> str:
    parts: list[str] = []
    if skill_content.strip():
        parts.append(
            "## Skill Knowledge\n"
            "Use these learned strategies when choosing the next action.\n\n"
            f"{skill_content.strip()}"
        )
    parts.append(observation.strip())
    if diagnostic_instruction.strip():
        parts.append(f"## Training Readout\n{diagnostic_instruction.strip()}")
    return "\n\n".join(part for part in parts if part.strip())


def _normalize_agent_response(raw: str | dict[str, Any]) -> str:
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, dict):
        content = raw.get("content")
        if isinstance(content, str):
            return content.strip()
    return ""


def _default_fallback_response(reason: str) -> str:
    return f"<think>{reason}</think><action>look</action>"


def run_alfworld_episode(
    *,
    backend: ALFWorldAgentBackend,
    environment: ALFWorldEpisodeEnvironment,
    skill_content: str = "",
    max_steps: int = 50,
    diagnostic_instruction: str = "",
) -> dict[str, Any]:
    try:
        initial = environment.reset()
        observation = str(initial.get("observation") or initial.get("text") or "").strip()
        gamefile = str(initial.get("gamefile") or "").strip()
        task_type = str(initial.get("task_type") or _infer_task_type_from_gamefile(gamefile))
        task_description = str(initial.get("task_description") or initial.get("goal") or observation).strip()
        messages: list[dict[str, Any]] = []
        trajectory: list[dict[str, Any]] = []
        won = False
        last_observation = observation

        for step_idx in range(max_steps):
            user_prompt = build_alfworld_user_prompt(
                observation=last_observation,
                skill_content=skill_content,
                diagnostic_instruction=diagnostic_instruction,
            )
            messages.append({"role": "user", "content": user_prompt})
            raw_response = backend.respond(
                system=ALFWORLD_SYSTEM_PROMPT,
                user=user_prompt,
                messages=list(messages),
            )
            response = _normalize_agent_response(raw_response)
            if not response:
                response = _default_fallback_response("empty model response")
            action = extract_action(response)
            if not action:
                response = _default_fallback_response("missing action tag")
                action = "look"
            reasoning = extract_think(response) or ""
            messages.append({"role": "assistant", "content": response})

            step_result = environment.step(action)
            last_observation = str(step_result.get("observation") or step_result.get("text") or "").strip()
            reward = float(step_result.get("reward") or 0.0)
            done = bool(step_result.get("done", False))
            won = bool(step_result.get("won", False))
            trajectory.append(
                {
                    "step": step_idx,
                    "action": action,
                    "reasoning": reasoning,
                    "model_response": response,
                    "env_feedback": last_observation,
                    "reward": reward,
                    "done": done,
                }
            )
            if done:
                break

        completed = bool(trajectory and trajectory[-1].get("done"))
        fail_reason = ""
        if not won:
            fail_reason = "Episode ended without completing the task" if completed else f"Timeout after {max_steps} steps"
        payload = {
            "predicted_answer": "<answer>success</answer>" if won else "<answer>fail</answer>",
            "hard": 1 if won else 0,
            "soft": 1.0 if won else 0.0,
            "n_turns": len(trajectory),
            "fail_reason": fail_reason,
            "agent_ok": True,
            "task_type": task_type,
            "gamefile": gamefile,
            "task_description": task_description,
            "instruction_type": task_type,
            "conversation": trajectory,
        }
        return {
            "prediction": json.dumps(payload, ensure_ascii=False),
            "payload": payload,
            "conversation": trajectory,
            "messages": messages,
        }
    finally:
        close = getattr(environment, "close", None)
        if callable(close):
            close()


def parse_success(prediction: str) -> bool:
    payload = _load_prediction_payload(prediction)
    if payload is not None:
        hard = payload.get("hard")
        if isinstance(hard, (int, float)):
            return bool(hard)
        predicted_answer = str(payload.get("predicted_answer") or "")
        if predicted_answer:
            prediction = predicted_answer
    answer = extract_answer(prediction).strip().lower()
    if answer in {"success", "completed", "complete", "done", "won", "pass", "1", "true", "yes"}:
        return True
    if answer in {"fail", "failed", "timeout", "0", "false", "no"}:
        return False
    if "success" in answer or "completed" in answer:
        return True
    return False


class ALFWorldEvaluator(SkillEvaluator):
    def evaluate(self, prediction: str, sample: SkillSample) -> MetricResult:
        payload = _load_prediction_payload(prediction)
        won = parse_success(prediction)
        task_type = str(sample.metadata.get("task_type") or "alfworld")
        gamefile = str(sample.metadata.get("gamefile") or "")
        task_description = str(sample.metadata.get("task_description") or sample.prompt)
        details: dict[str, Any] = {
            "hard": 1 if won else 0,
            "soft": 1.0 if won else 0.0,
            "task_type": task_type,
            "gamefile": gamefile,
            "task_description": task_description,
            "predicted_answer": extract_answer(prediction),
            "mode": "text",
        }
        if payload is not None:
            details.update(
                {
                    "hard": int(payload.get("hard", 1 if won else 0)),
                    "soft": float(payload.get("soft", 1.0 if won else 0.0)),
                    "task_type": str(payload.get("task_type") or task_type),
                    "gamefile": str(payload.get("gamefile") or gamefile),
                    "task_description": str(payload.get("task_description") or task_description),
                    "predicted_answer": str(payload.get("predicted_answer") or details["predicted_answer"]),
                    "n_turns": int(payload.get("n_turns", 0)),
                    "fail_reason": str(payload.get("fail_reason") or ""),
                    "agent_ok": bool(payload.get("agent_ok", True)),
                    "conversation": payload.get("conversation") if isinstance(payload.get("conversation"), list) else [],
                    "mode": "runtime_bundle",
                }
            )
        return MetricResult(
            score=1.0 if won else 0.0,
            passed=won,
            details=details,
        )
