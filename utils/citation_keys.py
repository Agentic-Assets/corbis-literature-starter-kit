"""Check LaTeX citation keys against a BibTeX file.

This checks key coverage only. Corbis ``verify_bibtex`` verifies record metadata.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ENTRY_RE = re.compile(r"@(?!(?:string|preamble|comment)\b)[A-Za-z]+\s*[({]\s*([^,\s]+)\s*,", re.I)
CITE_RE = re.compile(
    r"\\(?:cite|citep|citet|citealt|citealp|citeauthor|citeyear|citeyearpar)"
    r"\*?(?:\[[^\]]*\]){0,2}\s*\{([^}]*)\}"
)
INCLUDE_RE = re.compile(r"\\(?:input|include)\s*\{([^}]*)\}")


def strip_comments(source: str) -> str:
    """Remove LaTeX comments while retaining escaped percent signs."""
    lines = []
    for line in source.splitlines():
        for index, char in enumerate(line):
            if char == "%":
                backslashes = 0
                cursor = index - 1
                while cursor >= 0 and line[cursor] == "\\":
                    backslashes += 1
                    cursor -= 1
                if backslashes % 2 == 0:
                    line = line[:index]
                    break
        lines.append(line)
    return "\n".join(lines)


def bib_keys(path: Path) -> set[str]:
    return set(ENTRY_RE.findall(strip_comments(path.read_text(encoding="utf-8"))))


def tex_keys(path: Path, visited: set[Path] | None = None) -> tuple[set[str], set[Path]]:
    visited = visited if visited is not None else set()
    path = path.resolve()
    if path in visited:
        return set(), visited
    visited.add(path)
    source = strip_comments(path.read_text(encoding="utf-8"))
    keys = {key.strip() for group in CITE_RE.findall(source) for key in group.split(",") if key.strip()}
    for include in INCLUDE_RE.findall(source):
        child = path.parent / include.strip()
        if not child.suffix:
            child = child.with_suffix(".tex")
        if child.is_file():
            child_keys, _ = tex_keys(child, visited)
            keys.update(child_keys)
    return keys, visited


def audit(bib: Path, tex: Path | None = None) -> dict[str, object]:
    available = bib_keys(bib)
    if tex is None:
        return {"bibliography": str(bib), "bib_entries": len(available), "keys": sorted(available)}
    cited, files = tex_keys(tex)
    return {
        "bibliography": str(bib),
        "manuscript_files": sorted(str(path) for path in files),
        "bib_entries": len(available),
        "cited_keys": sorted(cited),
        "missing_keys": sorted(cited - available),
        "unused_entries": sorted(available - cited),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check LaTeX citation keys against a BibTeX file")
    parser.add_argument("bib", type=Path, help="BibTeX file to inspect")
    parser.add_argument("--tex", type=Path, help="Optional main LaTeX manuscript")
    args = parser.parse_args()
    try:
        result = audit(args.bib, args.tex)
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f"Citation key check failed: {exc}\n")
    print(json.dumps(result, indent=2))
    return 1 if result.get("missing_keys") else 0


if __name__ == "__main__":
    raise SystemExit(main())
