from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from darwinSkill.src.config_loader import (
    build_reference_adapter_from_config,
    build_samples,
    build_training_config,
    load_config,
)


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

    def test_build_reference_adapter_from_config_supports_inline_records(self) -> None:
        adapter = build_reference_adapter_from_config(
            {
                "benchmark": {"name": "office_qa"},
                "records": [{"question": "Capital of France?", "answer": "Paris"}],
            }
        )
        self.assertEqual(len(adapter.get_train_samples()), 1)
        self.assertEqual(adapter.benchmark.name, "officeqa")

    def test_build_reference_adapter_from_config_supports_relative_dataset_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            train_dir = root / "train"
            val_dir = root / "val"
            test_dir = root / "test"
            train_dir.mkdir()
            val_dir.mkdir()
            test_dir.mkdir()
            train_payload = [{"question": "Capital of France?", "answers": ["Paris"]}]
            val_payload = [{"question": "Largest planet?", "answers": ["Jupiter"]}]
            test_payload = [{"question": "Smallest planet?", "answers": ["Mercury"]}]
            (train_dir / "items.json").write_text(json.dumps(train_payload), encoding="utf-8")
            (val_dir / "items.json").write_text(json.dumps(val_payload), encoding="utf-8")
            (test_dir / "items.json").write_text(json.dumps(test_payload), encoding="utf-8")

            adapter = build_reference_adapter_from_config(
                {
                    "env": {"name": "search_qa", "data_path": "."},
                },
                base_dir=root,
            )
            self.assertEqual(adapter.benchmark.name, "searchqa")
            self.assertEqual(adapter.get_train_samples()[0].expected_answer, "Paris")
            self.assertEqual(adapter.get_eval_samples()[0].expected_answer, "Jupiter")


if __name__ == "__main__":
    unittest.main()
