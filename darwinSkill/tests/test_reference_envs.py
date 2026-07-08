from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from darwinSkill.src.docvqa_env import DocVQAEvaluator, load_docvqa_dataset
from darwinSkill.src.officeqa_env import OfficeQAEvaluator, load_officeqa_dataset
from darwinSkill.src.reference_adapters import DocVQAAdapter, OfficeQAAdapter, SearchQAAdapter
from darwinSkill.src.searchqa_env import SearchQAEvaluator, load_searchqa_dataset


class ReferenceEnvTest(unittest.TestCase):
    def test_searchqa_loader_and_evaluator_follow_reference_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for split, city in (("train", "Paris"), ("val", "Rome"), ("test", "Berlin")):
                split_dir = root / split
                split_dir.mkdir(parents=True)
                (split_dir / "items.json").write_text(
                    json.dumps(
                        [
                            {
                                "id": split,
                                "question": f"Capital for {split}?",
                                "context": "dummy",
                                "answers": [city, city.lower()],
                            }
                        ]
                    ),
                    encoding="utf-8",
                )
            train_records, eval_records = load_searchqa_dataset(root)
            self.assertEqual(train_records[0]["answers"][0], "Paris")
            self.assertEqual(eval_records[0]["answers"][0], "Rome")
            adapter = SearchQAAdapter.from_path(str(root))
            metric = SearchQAEvaluator().evaluate("<answer>paris</answer>", adapter.train_samples[0])
            self.assertTrue(metric.passed)
            self.assertEqual(metric.details["f1"], 1.0)

    def test_docvqa_loader_and_evaluator_follow_reference_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for split, answer in (("train", "Invoice 42"), ("val", "Memo 17"), ("test", "Report 3")):
                split_dir = root / split
                split_dir.mkdir(parents=True)
                with (split_dir / "items.csv").open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=["questionId", "question", "answer", "image_path", "topic"])
                    writer.writeheader()
                    writer.writerow(
                        {
                            "questionId": split,
                            "question": f"What doc is this? document_path:{split}.png",
                            "answer": json.dumps([answer]),
                            "image_path": f"{split}.png",
                            "topic": "forms",
                        }
                    )
            train_records, eval_records = load_docvqa_dataset(root)
            self.assertEqual(train_records[0]["image_path"], "train.png")
            self.assertEqual(eval_records[0]["answer"], "Memo 17")
            adapter = DocVQAAdapter.from_path(str(root))
            metric = DocVQAEvaluator().evaluate("<answer>invoice 42</answer>", adapter.train_samples[0])
            self.assertTrue(metric.passed)
            self.assertGreaterEqual(metric.score, 0.999)

    def test_officeqa_loader_and_evaluator_follow_reference_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for split, answer in (("train", "1,200 dollars"), ("val", "300"), ("test", "14%")):
                split_dir = root / split
                split_dir.mkdir(parents=True)
                with (split_dir / "items.csv").open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(
                        handle,
                        fieldnames=["uid", "question", "ground_truth", "category", "source_files", "source_docs"],
                    )
                    writer.writeheader()
                    writer.writerow(
                        {
                            "uid": split,
                            "question": f"Question {split}?",
                            "ground_truth": answer,
                            "category": "finance",
                            "source_files": json.dumps([f"{split}.txt"]),
                            "source_docs": json.dumps([f"Doc {split}"]),
                        }
                    )
            train_records, eval_records = load_officeqa_dataset(root)
            self.assertEqual(train_records[0]["source_files"], ["train.txt"])
            self.assertEqual(eval_records[0]["ground_truth"], "300")
            adapter = OfficeQAAdapter.from_path(str(root))
            metric = OfficeQAEvaluator().evaluate("<answer>1200</answer>", adapter.train_samples[0])
            self.assertTrue(metric.passed)
            self.assertEqual(metric.details["f1"], 1.0)


if __name__ == "__main__":
    unittest.main()
