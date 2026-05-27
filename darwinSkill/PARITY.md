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
- native benchmark helpers:
  - `run_reference_benchmark(...)`
  - `run_reference_adapter(...)`
  - evaluator benchmark-specific duoc auto resolve cho ca pack A va pack B
- split-aware adapter path:
  - `train_samples` dung cho reflective step loop
  - `eval_samples` dung cho gate/final report khi adapter co split rieng

## Con thieu

- provider/runtime compatibility hien o muc routing + injection contracts, chua gom client/runtime wrappers day du cho tung provider
- prompt/runtime behavior parity voi upstream rollout modules van con mot khoang cach o cac env tool-heavy:
  - `ALFWorld` simulator runtime
  - `SpreadsheetBench` codegen/react execution path
- artifact semantics hien da du cho native Python runs, nhung chua mirror tat ca trajectory formats upstream

## Khac biet co y

- khong co `__init__.py` package surface; dung module tree Python thuong
- khong giu CLI
- khong giu WebUI
- giu artifact inspectability bang file outputs, thay vi layer van hanh rieng
