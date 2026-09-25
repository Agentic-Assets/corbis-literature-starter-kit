import json
import tempfile
import unittest
from pathlib import Path

from utils.paper_set import merge, read_papers, select, write_papers


class PaperSetTests(unittest.TestCase):
    def test_merge_preserves_provenance_and_topic_selection(self):
        existing = [
            {"id": "W1", "title": "Shared paper", "abstract": "Existing abstract", "topics": ["climate"], "source_queries": ["old query"]},
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
        self.assertEqual([paper["id"] for paper in select(result, "insurance")], ["W1", "W3"])
        self.assertEqual([paper["id"] for paper in select(result, "banking")], ["W2"])

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


if __name__ == "__main__":
    unittest.main()
