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
- native benchmark helpers:
  - `run_reference_benchmark(...)`
  - `run_reference_adapter(...)`
  - evaluator benchmark-specific duoc auto resolve cho 3 env tren

## Con thieu

- benchmark pack B chua parity day du:
  - `ALFWorld`
  - `SpreadsheetBench`
  - `LiveMathematicianBench`
- provider/runtime compatibility hien o muc routing + injection contracts, chua gom client/runtime wrappers day du cho tung provider
- prompt/runtime behavior parity voi upstream rollout modules van con mot khoang cach o cac env tool-heavy

## Khac biet co y

- khong co `__init__.py` package surface; dung module tree Python thuong
- khong giu CLI
- khong giu WebUI
- giu artifact inspectability bang file outputs, thay vi layer van hanh rieng
