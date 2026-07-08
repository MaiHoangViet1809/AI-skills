from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from darwinSkill.src.extraction import build_trainable_examples
from darwinSkill.src.provider_logs import read_provider_session


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract trainable skill-improvement examples from canonical raw evidence.")
    parser.add_argument("--input", required=True, help="Path to canonical provider session artifact JSON.")
    parser.add_argument("--output", required=True, help="Path to write extracted examples JSON.")
    parser.add_argument("--skill-name", default="", help="Optional skill name override.")
    args = parser.parse_args()

    session = read_provider_session(Path(args.input))
    examples = build_trainable_examples(session, skill_name=args.skill_name)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([asdict(example) for example in examples], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
