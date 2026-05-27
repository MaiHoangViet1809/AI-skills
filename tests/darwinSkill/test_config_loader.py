from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from darwinSkill.config_loader import build_samples, build_training_config, load_config


class ConfigLoaderTest(unittest.TestCase):
    def test_yaml_config_inheritance_and_training_config_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            base = temp_root / "base.yaml"
            child = temp_root / "child.yaml"
            base.write_text(
                "train:\n  num_epochs: 3\n  batch_size: 2\noptimizer:\n  learning_rate: 5\nenv:\n  out_root: outputs/base\n",
                encoding="utf-8",
            )
            child.write_text(
                "_base_: base.yaml\ntrain:\n  run_name: inherited-run\noptimizer:\n  use_meta_skill: false\n",
                encoding="utf-8",
            )

            payload = load_config(child)
            config = build_training_config(payload)

            self.assertEqual(config.num_epochs, 3)
            self.assertEqual(config.batch_size, 2)
            self.assertEqual(config.edit_budget, 5)
            self.assertEqual(config.run_name, "inherited-run")
            self.assertFalse(config.use_meta_skill)

    def test_build_samples_from_records(self) -> None:
        samples = build_samples(
            [
                {"prompt": "Capital of France?", "expected_answer": "Paris"},
                {"prompt": "2 + 2 = ?", "expected_answer": "4", "metadata": {"kind": "math"}},
            ]
        )
        self.assertEqual(len(samples), 2)
        self.assertEqual(samples[1].metadata["kind"], "math")


if __name__ == "__main__":
    unittest.main()

