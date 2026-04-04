"""
Literature Landscape — Generate figures that visualize patterns in an academic literature.

Usage:
    python utils/lit_landscape.py data.json --figures timeline citations journals themes methods gapmap

Input: JSON file with array of paper objects. Each paper needs at minimum:
    {
        "title": "...",
        "authors": ["..."],
        "year": 2005,
        "journal": "...",
        "citedByCount": 1234,
        "abstract": "..."
    }

Optional fields: "id", "doi", "methods" (list), "setting" (str), "mechanism" (str)

Output: PDF figures saved to the same directory as the input file, or to --outdir.
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------

# Okabe-Ito colorblind-safe palette
OI_COLORS = [
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#009E73",  # bluish green
    "#F0E442",  # yellow
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#CC79A7",  # reddish purple
    "#999999",  # grey
]

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
    }
)

# ---------------------------------------------------------------------------
# Stopwords for keyword extraction
# ---------------------------------------------------------------------------

STOPWORDS = set(
    "the a an and or but in on of to for with from by is are was were be been "
    "being have has had do does did will would shall should may might can could "
    "this that these those it its we our they their them he she his her "
    "at as not no nor so if than more most very also however such which who whom "
    "what when where how all each both few many much some any between through "
    "during before after above below up down out off over under again further "
    "then once here there about into too only own same just because even still "
    "already while since until upon whether although though either neither yet "
    "using used use paper study find show results evidence effect effects based "
    "model data analysis provide suggest finds shows examine examines investigate "
    "demonstrate argues argue article two first second new among well across "
    "among within without however moreover furthermore therefore thus hence "
    "associated relationship related large small high low significant positive "
    "negative increase decrease higher lower increase decrease level levels "
    "approach approaches measure measures variable variables sample period "
    "test tests result consistent inconsistent important importantly "
    "existing prior recent literature review finding findings following".split()
)

# ---------------------------------------------------------------------------
# Method keywords for detection in abstracts
# ---------------------------------------------------------------------------

METHOD_PATTERNS = {
    "Diff-in-Diff": [
        r"difference.in.difference",
        r"\bdid\b",
        r"diff.in.diff",
        r"staggered.treatment",
        r"parallel.trend",
    ],
    "Event study": [
        r"event.study",
        r"abnormal.return",
        r"cumulative.abnormal",
        r"\bcar\b",
        r"\bcar[s]?\b",
    ],
    "IV / 2SLS": [
        r"instrumental.variable",
        r"\b2sls\b",
        r"two.stage.least.square",
        r"\biv\b.regression",
        r"\biv\b.estimat",
    ],
    "RDD": [
        r"regression.discontinuity",
        r"\brdd\b",
        r"\brd\b.design",
        r"close.election",
        r"threshold",
    ],
    "Panel / FE": [
        r"fixed.effect",
        r"panel.data",
        r"panel.regression",
        r"firm.fixed",
        r"year.fixed",
    ],
    "Cross-section": [
        r"cross.section",
        r"ols\b",
        r"ordinary.least.square",
    ],
    "Structural": [
        r"structural.model",
        r"structural.estimation",
        r"calibrat",
        r"general.equilibrium",
    ],
    "Natural experiment": [
        r"natural.experiment",
        r"quasi.experiment",
        r"exogenous.shock",
        r"plausibly.exogenous",
    ],
}

# ---------------------------------------------------------------------------
# Setting / geography keywords
# ---------------------------------------------------------------------------

SETTING_PATTERNS = {
    "United States": [r"\bu\.?s\.?\b", r"united.states", r"american"],
    "China": [r"\bchina\b", r"\bchinese\b"],
    "Europe": [r"\beurope\b", r"\beuropean\b", r"\beu\b"],
    "Emerging markets": [r"emerging.market", r"developing.countr"],
    "Cross-country": [r"cross.country", r"multiple.countr", r"\b\d+.countr"],
    "UK": [r"\bu\.?k\.?\b", r"united.kingdom", r"\bbritish\b"],
    "Japan": [r"\bjapan\b", r"\bjapanese\b"],
    "India": [r"\bindia\b", r"\bindian\b"],
    "Brazil": [r"\bbrazil\b", r"\bbrazilian\b"],
    "Other": [],
}

# ---------------------------------------------------------------------------
# Data loading and feature extraction
# ---------------------------------------------------------------------------


def load_papers(path: str) -> pd.DataFrame:
    """Load papers from JSON file into a DataFrame."""
    with open(path) as f:
        papers = json.load(f)

    df = pd.DataFrame(papers)

    # Ensure required columns exist
    for col in ["title", "year", "journal", "citedByCount", "abstract"]:
        if col not in df.columns:
            if col == "citedByCount":
                df[col] = 0
            elif col == "abstract":
                df[col] = ""
            else:
                df[col] = "Unknown"

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["citedByCount"] = pd.to_numeric(df["citedByCount"], errors="coerce").fillna(0)
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    return df


def extract_keywords(abstracts: pd.Series, top_n: int = 30) -> list[tuple[str, int]]:
    """Extract top bigrams from abstracts, excluding stopwords."""
    bigram_counts: Counter = Counter()
    for abstract in abstracts.dropna():
        words = re.findall(r"[a-z]+", abstract.lower())
        words = [w for w in words if w not in STOPWORDS and len(w) > 2]
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]
        bigram_counts.update(bigrams)
    return bigram_counts.most_common(top_n)


def detect_methods(abstract: str) -> list[str]:
    """Detect research methods mentioned in an abstract."""
    if not abstract or pd.isna(abstract):
        return []
    text = abstract.lower()
    found = []
    for method, patterns in METHOD_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text):
                found.append(method)
                break
    return found


def detect_setting(abstract: str) -> str:
    """Detect geographic setting mentioned in an abstract."""
    if not abstract or pd.isna(abstract):
        return "Other"
    text = abstract.lower()
    for setting, patterns in SETTING_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text):
                return setting
    return "Other"


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add method and setting columns to the DataFrame."""
    df = df.copy()
    df["methods"] = df["abstract"].apply(detect_methods)
    df["setting"] = df["abstract"].apply(detect_setting)
    return df


# ---------------------------------------------------------------------------
# Figure generators
# ---------------------------------------------------------------------------


def fig_timeline(df: pd.DataFrame, outdir: Path, group_by: str = "none"):
    """Publication count by year, optionally stacked by journal or setting."""
    fig, ax = plt.subplots(figsize=(10, 5))

    if group_by == "journal":
        top_journals = df["journal"].value_counts().head(6).index.tolist()
        df_plot = df.copy()
        df_plot.loc[~df_plot["journal"].isin(top_journals), "journal"] = "Other"
        ct = df_plot.groupby(["year", "journal"]).size().unstack(fill_value=0)
        # Sort columns by total count descending
        ct = ct[ct.sum().sort_values(ascending=False).index]
        ct.plot.bar(stacked=True, ax=ax, color=OI_COLORS[: len(ct.columns)], width=0.8)
        ax.legend(fontsize=8, loc="upper left", frameon=False)
    else:
        counts = df.groupby("year").size()
        ax.bar(counts.index, counts.values, color=OI_COLORS[4], width=0.8)

    ax.set_xlabel("Year")
    ax.set_ylabel("Number of papers")
    ax.set_title("Publication Volume Over Time")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=15))
    plt.xticks(rotation=45, ha="right")

    path = outdir / "fig_timeline.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig_citations(df: pd.DataFrame, outdir: Path, label_top_n: int = 8):
    """Citation landmark chart: year vs citedByCount, top papers labeled."""
    fig, ax = plt.subplots(figsize=(10, 6))

    sizes = np.clip(df["citedByCount"].values / 10, 10, 500)
    ax.scatter(
        df["year"],
        df["citedByCount"],
        s=sizes,
        alpha=0.6,
        color=OI_COLORS[4],
        edgecolors="white",
        linewidth=0.5,
    )

    # Label top papers
    top = df.nlargest(label_top_n, "citedByCount")
    for _, row in top.iterrows():
        # Short label: first author + year
        authors = row.get("authors", [])
        if isinstance(authors, list) and len(authors) > 0:
            first = authors[0].split(",")[0].split()[-1]
        else:
            first = "?"
        label = f"{first} ({int(row['year'])})"
        ax.annotate(
            label,
            (row["year"], row["citedByCount"]),
            fontsize=7,
            ha="left",
            va="bottom",
            xytext=(5, 5),
            textcoords="offset points",
        )

    ax.set_xlabel("Year")
    ax.set_ylabel("Citation count")
    ax.set_title("Citation Landmark Chart")
    ax.set_yscale("symlog", linthresh=10)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    path = outdir / "fig_citations.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig_journals(df: pd.DataFrame, outdir: Path, top_n: int = 12):
    """Horizontal bar chart of journal distribution."""
    fig, ax = plt.subplots(figsize=(8, 5))

    counts = df["journal"].value_counts().head(top_n).sort_values()
    ax.barh(counts.index, counts.values, color=OI_COLORS[2])
    ax.set_xlabel("Number of papers")
    ax.set_title("Journal Distribution")

    for i, v in enumerate(counts.values):
        ax.text(v + 0.3, i, str(v), va="center", fontsize=9)

    path = outdir / "fig_journals.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig_themes(df: pd.DataFrame, outdir: Path, top_n: int = 15, bin_size: int = 3):
    """Thematic evolution heatmap: keyword frequency across year bins."""
    # Create year bins
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    bins = list(range(min_year, max_year + bin_size, bin_size))
    bin_labels = [f"{b}-{min(b + bin_size - 1, max_year)}" for b in bins[:-1]]
    if not bin_labels:
        bin_labels = [f"{min_year}-{max_year}"]
        bins = [min_year, max_year + 1]

    df_copy = df.copy()
    df_copy["year_bin"] = pd.cut(
        df_copy["year"], bins=bins, labels=bin_labels[: len(bins) - 1], right=False
    )

    # Get top keywords across all abstracts
    top_keywords = extract_keywords(df["abstract"], top_n=top_n)
    keyword_list = [kw for kw, _ in top_keywords]

    # Build the matrix
    matrix = []
    for kw in keyword_list:
        row = []
        for label in bin_labels[: len(bins) - 1]:
            subset = df_copy[df_copy["year_bin"] == label]
            count = sum(
                1
                for abstract in subset["abstract"].dropna()
                if kw in abstract.lower()
            )
            row.append(count)
        matrix.append(row)

    matrix = np.array(matrix)
    if matrix.size == 0:
        print("  Skipped fig_themes: not enough data")
        return None

    fig, ax = plt.subplots(figsize=(10, max(5, top_n * 0.35)))
    im = ax.imshow(matrix, aspect="auto", cmap="YlOrRd")

    ax.set_xticks(range(len(bin_labels[: len(bins) - 1])))
    ax.set_xticklabels(bin_labels[: len(bins) - 1], rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(keyword_list)))
    ax.set_yticklabels(keyword_list, fontsize=8)
    ax.set_title("Thematic Evolution")

    # Add count annotations
    for i in range(len(keyword_list)):
        for j in range(matrix.shape[1]):
            val = matrix[i, j]
            if val > 0:
                color = "white" if val > matrix.max() * 0.6 else "black"
                ax.text(j, i, str(val), ha="center", va="center", fontsize=7, color=color)

    fig.colorbar(im, ax=ax, shrink=0.6, label="Paper count")

    path = outdir / "fig_themes.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig_methods(df: pd.DataFrame, outdir: Path, bin_size: int = 3):
    """Methods evolution: stacked area of identification strategies over time."""
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    bins = list(range(min_year, max_year + bin_size, bin_size))
    bin_labels = [f"{b}-{min(b + bin_size - 1, max_year)}" for b in bins[:-1]]
    if not bin_labels:
        print("  Skipped fig_methods: not enough year range")
        return None

    df_copy = df.copy()
    df_copy["year_bin"] = pd.cut(
        df_copy["year"], bins=bins, labels=bin_labels[: len(bins) - 1], right=False
    )

    methods_list = list(METHOD_PATTERNS.keys())
    data = defaultdict(list)
    for label in bin_labels[: len(bins) - 1]:
        subset = df_copy[df_copy["year_bin"] == label]
        for method in methods_list:
            count = sum(1 for methods in subset["methods"] if method in methods)
            data[method].append(count)

    # Filter out methods with zero total
    active_methods = [m for m in methods_list if sum(data[m]) > 0]
    if not active_methods:
        print("  Skipped fig_methods: no methods detected in abstracts")
        return None

    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(bin_labels[: len(bins) - 1]))
    bottom = np.zeros(len(x))

    for i, method in enumerate(active_methods):
        values = np.array(data[method])
        ax.bar(
            x,
            values,
            bottom=bottom,
            label=method,
            color=OI_COLORS[i % len(OI_COLORS)],
            width=0.8,
        )
        bottom += values

    ax.set_xticks(list(x))
    ax.set_xticklabels(bin_labels[: len(bins) - 1], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Number of papers")
    ax.set_title("Research Methods Over Time")
    ax.legend(fontsize=8, loc="upper left", frameon=False)

    path = outdir / "fig_methods.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig_gapmap(
    df: pd.DataFrame,
    outdir: Path,
    row_dim: str = "setting",
    col_dim: str = "methods",
    row_labels: list[str] | None = None,
    col_labels: list[str] | None = None,
):
    """Coverage gap map: matrix of paper counts by two dimensions."""
    if row_dim == "setting" and row_labels is None:
        row_labels = [s for s in SETTING_PATTERNS.keys() if s != "Other"]
        # Only keep settings with at least 1 paper
        row_labels = [s for s in row_labels if (df["setting"] == s).any()]
        row_labels.append("Other")

    if col_dim == "methods" and col_labels is None:
        col_labels = list(METHOD_PATTERNS.keys())
        # Only keep methods with at least 1 paper
        col_labels = [
            m
            for m in col_labels
            if df["methods"].apply(lambda ms: m in ms).any()
        ]

    if not row_labels or not col_labels:
        print("  Skipped fig_gapmap: insufficient dimension labels")
        return None

    # Build the matrix
    matrix = np.zeros((len(row_labels), len(col_labels)), dtype=int)
    for i, rl in enumerate(row_labels):
        for j, cl in enumerate(col_labels):
            if row_dim == "setting":
                row_mask = df["setting"] == rl
            else:
                row_mask = df["abstract"].str.lower().str.contains(rl.lower(), na=False)

            if col_dim == "methods":
                col_mask = df["methods"].apply(lambda ms: cl in ms)
            else:
                col_mask = df["abstract"].str.lower().str.contains(cl.lower(), na=False)

            matrix[i, j] = (row_mask & col_mask).sum()

    fig, ax = plt.subplots(figsize=(max(7, len(col_labels) * 1.2), max(4, len(row_labels) * 0.6)))

    # Custom colormap: 0 = highlighted red/pink (gap), higher = green
    from matplotlib.colors import LinearSegmentedColormap

    gap_cmap = LinearSegmentedColormap.from_list(
        "gap", ["#FFCCCC", "#FFFFFF", "#B8E6B8", "#2E8B57"], N=256
    )

    im = ax.imshow(matrix, aspect="auto", cmap=gap_cmap, vmin=0)

    ax.set_xticks(range(len(col_labels)))
    ax.set_xticklabels(col_labels, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(row_labels)))
    ax.set_yticklabels(row_labels, fontsize=9)
    ax.set_title("Coverage Gap Map")

    # Annotate cells
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            val = matrix[i, j]
            label = str(val) if val > 0 else "GAP"
            weight = "bold" if val == 0 else "normal"
            color = "#CC0000" if val == 0 else "black"
            ax.text(
                j, i, label, ha="center", va="center", fontsize=9, fontweight=weight, color=color
            )

    fig.colorbar(im, ax=ax, shrink=0.6, label="Paper count")

    path = outdir / "fig_gapmap.pdf"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

FIGURE_REGISTRY = {
    "timeline": ("Publication timeline", fig_timeline),
    "citations": ("Citation landmark chart", fig_citations),
    "journals": ("Journal distribution", fig_journals),
    "themes": ("Thematic evolution heatmap", fig_themes),
    "methods": ("Methods timeline", fig_methods),
    "gapmap": ("Coverage gap map", fig_gapmap),
}


def main():
    parser = argparse.ArgumentParser(description="Literature Landscape Figure Generator")
    parser.add_argument("data", help="Path to JSON file with paper metadata")
    parser.add_argument(
        "--figures",
        nargs="+",
        choices=list(FIGURE_REGISTRY.keys()) + ["all"],
        default=["all"],
        help="Which figures to generate (default: all)",
    )
    parser.add_argument("--outdir", help="Output directory (default: same as data file)")
    parser.add_argument("--group-timeline-by", choices=["none", "journal"], default="none")
    parser.add_argument("--bin-size", type=int, default=3, help="Year bin size for heatmaps")
    parser.add_argument("--label-top-n", type=int, default=8, help="Papers to label on citation chart")
    parser.add_argument(
        "--gapmap-rows",
        default="setting",
        help="Gap map row dimension: 'setting' (auto) or comma-separated custom labels",
    )
    parser.add_argument(
        "--gapmap-cols",
        default="methods",
        help="Gap map column dimension: 'methods' (auto) or comma-separated custom labels",
    )

    args = parser.parse_args()

    # Resolve figures
    if "all" in args.figures:
        figures = list(FIGURE_REGISTRY.keys())
    else:
        figures = args.figures

    # Load and process
    print(f"Loading papers from {args.data}...")
    df = load_papers(args.data)
    print(f"  {len(df)} papers loaded ({int(df['year'].min())}-{int(df['year'].max())})")

    df = extract_features(df)
    method_counts = df["methods"].apply(len).sum()
    setting_counts = (df["setting"] != "Other").sum()
    print(f"  Methods detected in {method_counts} paper-method pairs")
    print(f"  Geographic settings identified for {setting_counts} papers")

    outdir = Path(args.outdir) if args.outdir else Path(args.data).parent
    outdir.mkdir(parents=True, exist_ok=True)

    # Generate figures
    print(f"\nGenerating {len(figures)} figures...")
    for fig_key in figures:
        name, func = FIGURE_REGISTRY[fig_key]
        print(f"\n  [{fig_key}] {name}")
        try:
            if fig_key == "timeline":
                func(df, outdir, group_by=args.group_timeline_by)
            elif fig_key == "citations":
                func(df, outdir, label_top_n=args.label_top_n)
            elif fig_key == "themes":
                func(df, outdir, bin_size=args.bin_size)
            elif fig_key == "methods":
                func(df, outdir, bin_size=args.bin_size)
            elif fig_key == "gapmap":
                row_labels = None if args.gapmap_rows == "setting" else args.gapmap_rows.split(",")
                col_labels = None if args.gapmap_cols == "methods" else args.gapmap_cols.split(",")
                func(
                    df,
                    outdir,
                    row_dim="setting" if row_labels is None else "custom",
                    col_dim="methods" if col_labels is None else "custom",
                    row_labels=row_labels,
                    col_labels=col_labels,
                )
            else:
                func(df, outdir)
        except Exception as e:
            print(f"  ERROR generating {fig_key}: {e}")

    print(f"\nDone. Figures saved to {outdir}/")


if __name__ == "__main__":
    main()
