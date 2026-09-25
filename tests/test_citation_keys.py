import tempfile
import unittest
from pathlib import Path

from utils.citation_keys import audit


class CitationKeyAuditTests(unittest.TestCase):
    def test_full_bib_and_natbib_keys_across_included_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            bib = root / "references.bib"
            main = root / "paper.tex"
            section = root / "section.tex"
            bib.write_text(
                "@string{journal = {Journal}}\n"
                "% @article{commented, title={Ignored}}\n"
                "@article{alpha, title={A}}\n"
                "@article{beta, title={B}}\n"
                "@article{unused, title={C}}\n",
                encoding="utf-8",
            )
            main.write_text(
                "\\citet[see][p. 2]{alpha} % \\citep{commented}\n"
                "\\input{section}\n",
                encoding="utf-8",
            )
            section.write_text("\\citep{beta, missing}\\\\% text\n", encoding="utf-8")

            result = audit(bib, main)

            self.assertEqual(result["bib_entries"], 3)
            self.assertEqual(result["cited_keys"], ["alpha", "beta", "missing"])
            self.assertEqual(result["missing_keys"], ["missing"])
            self.assertEqual(result["unused_entries"], ["unused"])
            self.assertEqual(len(result["manuscript_files"]), 2)

    def test_bib_only_audits_every_entry(self):
        with tempfile.TemporaryDirectory() as folder:
            bib = Path(folder) / "references.bib"
            bib.write_text("@article{one, title={A}}\n@book{two, title={B}}\n", encoding="utf-8")
            result = audit(bib)
            self.assertEqual(result["keys"], ["one", "two"])
            self.assertEqual(result["bib_entries"], 2)


if __name__ == "__main__":
    unittest.main()
