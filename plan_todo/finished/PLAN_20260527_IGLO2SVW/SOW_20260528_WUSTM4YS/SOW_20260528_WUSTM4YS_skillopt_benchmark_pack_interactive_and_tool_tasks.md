# SOW_20260528_WUSTM4YS - skillopt benchmark pack interactive and tool tasks

- Status: completed
- Approval: approved
- create_dttm: 2026-05-28T01:05:05+07:00
- create_date: 2026-05-28
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260528_WUSTM4YS)
- approve_dttm: unknown
- finish_dttm: unknown
- legacy_id: SOW_0054
- legacy_path: plan_todo/SOW_0054_skillopt_benchmark_pack_interactive_and_tool_tasks.md
- migrated_dttm: 2026-10-08T12:48:51+07:00

## Preserved Contract And Historical Evidence

- **Status**: completed
- **Approval**: approved
- **Task**: Migrate benchmark pack thứ hai của reference SkillOpt gồm `ALFWorld`, `SpreadsheetBench`, và `LiveMathematicianBench`, bao gồm các runtime/tool needs và evaluator contracts phức tạp hơn.
- **Location**: `~/Projects/AISkills/darwinSkill/`, `~/Projects/AISkills/tests/darwinSkill/`, `~/Projects/AISkills/references/SkillOpt/skillopt/envs/alfworld/`, `~/Projects/AISkills/references/SkillOpt/skillopt/envs/spreadsheetbench/`, `~/Projects/AISkills/references/SkillOpt/skillopt/envs/livemathematicianbench/`
- **Why**: Đây là nhóm benchmark gần nhất với độ phức tạp thật của original project. Nếu không migrate nhóm này thì parity với original sẽ vẫn thiếu những execution paths khó nhất.
- **As-Is Diagram (ASCII)**:
```text
benchmark migration
  -> no interactive/tool-heavy env parity yet
```
- **To-Be Diagram (ASCII)**:
```text
darwinSkill benchmark pack B
  -> ALFWorld environment path
  -> SpreadsheetBench tool/codegen/react path
  -> LiveMathematicianBench path
  -> richer trajectory + evaluator handling
```
- **Deliverables**:
  - migrate or reconstruct adapters and runtime wiring for the three benchmark families
  - support tool/runtime-specific rollout artifacts required by these envs
  - add benchmark-scoped integration acceptance path and execution notes
  - isolate heavyweight or optional dependency handling so core framework remains importable
- **Done Criteria**:
  - the interactive/tool-heavy benchmark families have a credible execution path on top of `darwinSkill`
  - framework boundaries remain intact despite the more complex env requirements
  - heavy dependencies are documented and isolated cleanly
- **Progress Notes**:
  - added benchmark-native modules for:
    - `darwinSkill/alfworld_env.py`
    - `darwinSkill/spreadsheetbench_env.py`
    - `darwinSkill/livemathematician_env.py`
  - added acceptance tests for loader/evaluator/native adapter flow of the three benchmark families
  - `openpyxl` duoc add lam optional-runtime dependency thuc te cho SpreadsheetBench evaluator path
  - `SpreadsheetBench` evaluator da ho tro execute prediction dang Python code block de sinh workbook output va cham theo answer range
  - `SpreadsheetBench` evaluator da ho tro them structured JSON artifact bundle path cho `solution.py` / `output.xlsx`
  - `SpreadsheetBench` evaluator da ho tro them workspace bundle `files + commands`, phu hop hon voi react-like orchestration
  - `SpreadsheetBench` evaluator da ho tro them structured `tool_calls` bundle (`write_file` + `bash`)
  - `SpreadsheetBench` evaluator da ho tro them `react transcript` bundle co assistant turns + tool calls
  - `SpreadsheetBench` evaluator da ho tro them replay bundle theo shape rollout upstream: `conversation.json` + `solution.py` artifact/file
  - `SpreadsheetBench` da co native react-runner surface de backend callback sinh `conversation + solution.py` bundle ngay trong Python API
  - `ALFWorld` da co native episode-runner surface de backend callback + env shim sinh runtime bundle co trajectory
  - `ALFWorld` da co optional live environment factory de bridge vao reference vendor simulator neu local dependencies co san
  - `BackendRouter` da co target-role wrapper helpers cho `SpreadsheetBench` va `ALFWorld`, gan hon voi dual-role execution semantics cua upstream
  - da co provider-compat wrappers cho OpenAI/Claude/Qwen/Codex-style tool-call payloads de cap native runners bang format gan upstream hon
  - da co family-aware bootstrap helper de di tu benchmark + provider family -> interactive router
  - done criteria da dat o framework core; phan con lai neu co chu yeu la production dependency/auth/bootstrap ben ngoai core, khong phai khoang trong chuc nang cua native Python API
- **Out-of-Scope**:
  - UI parity
  - paper-metric reproduction
  - support for benchmark families outside the reference snapshot
- **Proposed-By**: Codex GPT-5
- **plan**: `plan_todo/finished/PLAN_20260527_IGLO2SVW/PLAN_20260527_IGLO2SVW_skill_framework_distillation_plan.md`
- **Cautions / Risks**:
  - đây là slice có blast radius lớn nhất về dependencies và execution runtime
  - cần tránh cho benchmark-specific hacks rò vào engine core
