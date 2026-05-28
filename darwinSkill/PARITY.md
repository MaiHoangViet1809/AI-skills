# darwinSkill parity snapshot

Muc tieu cua `darwinSkill` la functional parity o native Python API layer, khong phai clone CLI hay WebUI cua upstream.

## Da hoan tat

- reflective trainer core:
  - step gating
  - best-skill tracking
  - resume state
  - slow update
  - meta-skill epoch memory
- backend routing abstraction:
  - tach target role va optimizer role qua `BackendRouter`
  - co compatibility mapping cho cac family chinh trong reference snapshot
- benchmark pack A:
  - `SearchQA`
  - `DocVQA`
  - `OfficeQA`
  - moi env da co loader normalization, evaluator, va adapter path rieng
- benchmark pack B:
  - `ALFWorld`
  - `SpreadsheetBench`
  - `LiveMathematicianBench`
  - da co native loader/evaluator/adapter path va acceptance tests cho benchmark surface
  - `SpreadsheetBench` evaluator co the execute prediction dang Python code block de cham workbook output
  - `SpreadsheetBench` evaluator cung hieu structured JSON artifact bundle cho `solution.py` / `output.xlsx`
  - `SpreadsheetBench` evaluator co them workspace bundle path (`files + commands`) cho react-like orchestration
  - `SpreadsheetBench` evaluator co them structured `tool_calls` bundle (`write_file` + `bash`)
  - `SpreadsheetBench` evaluator co them `react transcript` bundle co assistant turns + tool calls
  - `SpreadsheetBench` evaluator co them upstream-style `conversation.json` replay path khi prediction bundle kem `solution.py` artifact/file
  - `SpreadsheetBench` co native react-runner helper de backend callback co the sinh `conversation + solution.py` prediction bundle
- native benchmark helpers:
  - `run_reference_benchmark(...)`
  - `run_reference_adapter(...)`
  - `run_reference_benchmark_from_path(...)`
  - evaluator benchmark-specific duoc auto resolve cho ca pack A va pack B
- split-aware adapter path:
  - `train_samples` dung cho reflective step loop
  - `eval_samples` dung cho gate/final report khi adapter co split rieng
- inspection helpers:
  - `inspect_run(...)`
  - `summarize_run(...)`
  - `load_step_record(...)`

## Con thieu

- provider/runtime compatibility hien o muc routing + injection contracts, chua gom client/runtime wrappers day du cho tung provider
- prompt/runtime behavior parity voi upstream rollout modules van con mot khoang cach o cac env tool-heavy:
  - `ALFWorld` simulator runtime
  - `SpreadsheetBench` provider-specific live react wrappers beyond native backend callback surface
- artifact semantics hien da du cho native Python runs, nhung chua mirror tat ca trajectory formats upstream

## Khac biet co y

- khong co `__init__.py` package surface; dung module tree Python thuong
- khong giu CLI
- khong giu WebUI
- giu artifact inspectability bang file outputs, thay vi layer van hanh rieng
