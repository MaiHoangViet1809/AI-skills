from __future__ import annotations

import argparse
from pathlib import Path

from darwinSkill.provider_logs import load_codex_session, write_provider_session


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize provider-native logs into darwinSkill canonical raw artifacts.")
    parser.add_argument("--provider", required=True, choices=["codex"])
    parser.add_argument("--input", required=True, help="Path to provider-native input log.")
    parser.add_argument("--output", required=True, help="Path to write canonical JSON artifact.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if args.provider == "codex":
        session = load_codex_session(input_path)
    else:  # pragma: no cover
        raise ValueError(f"Unsupported provider: {args.provider}")
    write_provider_session(output_path, session)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

