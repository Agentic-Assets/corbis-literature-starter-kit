"""Regression tests for the figure generator's input and completion contract."""

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import pandas as pd

from utils import lit_landscape as landscape


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "utils" / "lit_landscape.py"


class FigureTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.outdir = Path(self.tempdir.name)
        self.papers = pd.DataFrame(
            {
                "year": [2000, 2003],
                "abstract": [
                    "fixed effects reveal bank lending patterns",
                    "fixed effects reveal bank lending patterns",
                ],
                "methods": [["Panel / FE"], ["Panel / FE"]],
            }
        )

    def test_year_bins_include_boundary_and_single_year(self):
        bins, labels = landscape.year_bins(self.papers["year"], 3)
        self.assertEqual(bins, [2000, 2003, 2006])
        self.assertEqual(labels, ["2000-2002", "2003-2003"])
        assigned = pd.cut(self.papers["year"], bins=bins, labels=labels, right=False)
        self.assertEqual(assigned.tolist(), labels)
        self.assertEqual(landscape.year_bins(pd.Series([2003]), 3), ([2003, 2006], ["2003-2003"]))
        with self.assertRaisesRegex(ValueError, "positive integer"):
            landscape.year_bins(self.papers["year"], 0)

    def test_theme_and_method_figures_count_latest_boundary_year(self):
        # Keep figure objects alive long enough to inspect the plotted data.
        with mock.patch.object(landscape.plt, "close"):
            theme_path = landscape.fig_themes(self.papers, self.outdir, bin_size=3)
            theme_ax = plt.gcf().axes[0]
            theme_totals = list(theme_ax.images[0].get_array().sum(axis=0))
            self.assertEqual(theme_totals[0], theme_totals[1])
            self.assertGreater(theme_totals[1], 0)
            self.assertEqual(
                [tick.get_text() for tick in theme_ax.get_xticklabels()],
                ["2000-2002", "2003-2003"],
            )

            method_path = landscape.fig_methods(self.papers, self.outdir, bin_size=3)
            method_ax = plt.gcf().axes[0]
            self.assertEqual([patch.get_height() for patch in method_ax.patches], [1, 1])
            self.assertEqual(
                [tick.get_text() for tick in method_ax.get_xticklabels()],
                ["2000-2002", "2003-2003"],
            )
        plt.close("all")

        self.assertGreater(theme_path.stat().st_size, 0)
        self.assertGreater(method_path.stat().st_size, 0)

    def run_script(self, papers, *args):
        data_path = self.outdir / "papers.json"
        data_path.write_text(json.dumps(papers))
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(data_path), *args],
            capture_output=True,
            text=True,
            env={**os.environ, "MPLBACKEND": "Agg"},
            check=False,
        )

    def test_empty_and_yearless_inputs_fail_clearly(self):
        empty = self.run_script([], "--figures", "timeline")
        self.assertNotEqual(empty.returncode, 0)
        self.assertIn("nonempty JSON array", empty.stderr)
        self.assertNotIn("Done.", empty.stdout)

        yearless = self.run_script([{"title": "Unknown"}], "--figures", "timeline")
        self.assertNotEqual(yearless.returncode, 0)
        self.assertIn("No papers have a valid year", yearless.stderr)

    def test_nonpositive_bin_size_fails_before_plotting(self):
        result = self.run_script([{"year": 2000}], "--bin-size", "0")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--bin-size must be a positive integer", result.stderr)

    def test_figure_exception_and_skip_report_incomplete(self):
        data_path = self.outdir / "papers.json"
        data_path.write_text(json.dumps([{"year": 2000, "abstract": "fixed effects"}]))
        argv = [str(SCRIPT), str(data_path), "--figures", "timeline", "themes"]
        registry = {
            "timeline": ("timeline", mock.Mock(side_effect=RuntimeError("plot failed"))),
            "themes": ("themes", mock.Mock(return_value=None)),
        }
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "argv", argv), mock.patch.object(landscape, "FIGURE_REGISTRY", registry):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = landscape.main()
        self.assertEqual(code, 1)
        self.assertIn("ERROR generating timeline: plot failed", stderr.getvalue())
        self.assertIn("Figures not generated: timeline, themes", stderr.getvalue())
        self.assertNotIn("Done.", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
