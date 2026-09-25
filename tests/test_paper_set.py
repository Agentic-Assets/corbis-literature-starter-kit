import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from utils.paper_set import merge, read_papers, select, write_papers


SCRIPT = Path(__file__).resolve().parents[1] / "utils" / "paper_set.py"


class PaperSetTests(unittest.TestCase):
    def test_merge_preserves_provenance_and_topic_selection(self):
        existing = [
            {"id": "W1", "title": "Shared paper", "abstract": "Existing abstract", "topics": ["climate"], "source_queries": ["old query"], "tier": "foundational"},
            {"id": "W2", "title": "Unrelated paper", "topics": ["banking"]},
        ]
        incoming = [
            {"id": "W1", "title": "Shared paper", "abstract": None, "source_queries": ["new query"]},
            {"id": "W3", "title": "New paper", "year": 2024},
        ]

        result = merge(existing, incoming, "insurance", "new query")

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["abstract"], "Existing abstract")
        self.assertEqual(result[0]["topics"], ["climate", "insurance"])
        self.assertEqual(result[0]["source_queries"], ["old query", "new query"])
        self.assertEqual(result[0]["source_queries_by_topic"], {"insurance": ["new query"]})
        self.assertNotIn("tier", result[0])
        self.assertEqual([paper["id"] for paper in select(result, "insurance")], ["W1", "W3"])
        self.assertEqual([paper["id"] for paper in select(result, "banking")], ["W2"])

    def test_select_discards_legacy_global_tier(self):
        papers = [{"id": "W1", "title": "Shared", "topics": ["insurance"], "tier": "foundational"}]
        self.assertNotIn("tier", select(papers, "insurance")[0])

    def test_topic_query_count_does_not_include_other_topics(self):
        papers = merge([], [{"id": "W1", "title": "Shared"}], "climate", "climate one")
        papers = merge(papers, [{"id": "W1", "title": "Shared"}], "climate", "climate two")
        papers = merge(papers, [{"id": "W1", "title": "Shared"}], "insurance", "insurance one")
        self.assertEqual(len(papers[0]["source_queries"]), 3)
        self.assertEqual(papers[0]["source_queries_by_topic"]["insurance"], ["insurance one"])

    def test_read_accepts_mcp_results_and_rejects_invalid_ids(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "papers.json"
            path.write_text(json.dumps({"results": [{"id": "W1", "title": "Paper"}]}), encoding="utf-8")
            self.assertEqual(read_papers(path)[0]["id"], "W1")
            path.write_text(json.dumps([{"title": "No ID"}]), encoding="utf-8")
            with self.assertRaises(ValueError):
                read_papers(path)

    def test_write_then_read_preserves_unicode(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "paper_set.json"
            write_papers(path, [{"id": "W1", "title": "Yönder"}])
            self.assertEqual(read_papers(path)[0]["title"], "Yönder")

    def test_cli_missing_required_input_fails_without_writing_dataset(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            dataset = root / "paper_set.json"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "merge", "--dataset", str(dataset),
                 "--input", str(root / "missing.json"), "--topic", "banking"],
                capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Paper set operation failed", result.stderr)
            self.assertFalse(dataset.exists())

    def test_cli_merge_bootstraps_new_dataset_from_existing_input(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            dataset = root / "paper_set.json"
            incoming = root / "selected.json"
            incoming.write_text(json.dumps([{"id": "W1", "title": "Paper"}]), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "merge", "--dataset", str(dataset),
                 "--input", str(incoming), "--topic", "banking", "--query", "bank lending"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(read_papers(dataset)[0]["source_queries_by_topic"], {"banking": ["bank lending"]})

    def test_cli_missing_select_dataset_fails_without_writing_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            output = root / "selected.json"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "select", "--dataset", str(root / "missing.json"),
                 "--topic", "banking", "--output", str(output)],
                capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Paper set operation failed", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
