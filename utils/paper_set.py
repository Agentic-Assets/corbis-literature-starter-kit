"""Merge Corbis paper records and select a topic-scoped figure/review set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_papers(path: Path) -> list[dict]:
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, dict):
        value = value.get("results")
    if not isinstance(value, list) or any(not isinstance(paper, dict) for paper in value):
        raise ValueError(f"{path} must contain a paper array or an object with results[]")
    if any(not isinstance(paper.get("id"), str) or not paper["id"] for paper in value):
        raise ValueError(f"{path} contains a paper without an id")
    return value


def union_strings(*values: object) -> list[str]:
    result: list[str] = []
    for value in values:
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item and item not in result:
                    result.append(item)
        elif isinstance(value, str) and value and value not in result:
            result.append(value)
    return result


def merge(existing: list[dict], incoming: list[dict], topic: str, query: str | None = None) -> list[dict]:
    """Merge selected relevant incoming papers by ID without losing provenance."""
    merged = {paper["id"]: dict(paper) for paper in existing}
    for paper in incoming:
        paper_id = paper.get("id")
        if not isinstance(paper_id, str) or not paper_id or not paper.get("title"):
            raise ValueError("each incoming paper needs a nonempty id and title")
        prior = merged.get(paper_id, {})
        combined = dict(prior)
        combined.update({key: value for key, value in paper.items() if value not in (None, "", [])})
        combined["topics"] = union_strings(prior.get("topics"), paper.get("topics"), topic)
        combined["source_queries"] = union_strings(
            prior.get("source_queries"), paper.get("source_queries"), query
        )
        merged[paper_id] = combined
    return list(merged.values())


def select(papers: list[dict], topic: str) -> list[dict]:
    return [paper for paper in papers if isinstance(paper.get("topics"), list) and topic in paper["topics"]]


def write_papers(path: Path, papers: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(papers, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("--dataset", type=Path, default=Path("output/paper_set.json"))
    merge_parser.add_argument("--input", type=Path, required=True, help="JSON array of selected relevant papers")
    merge_parser.add_argument("--topic", required=True, help="Stable topic slug")
    merge_parser.add_argument("--query", help="Search query that surfaced these papers")
    select_parser = subparsers.add_parser("select")
    select_parser.add_argument("--dataset", type=Path, default=Path("output/paper_set.json"))
    select_parser.add_argument("--topic", required=True, help="Stable topic slug")
    select_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        papers = read_papers(args.dataset)
        if args.action == "merge":
            papers = merge(papers, read_papers(args.input), args.topic, args.query)
            write_papers(args.dataset, papers)
        else:
            papers = select(papers, args.topic)
            write_papers(args.output, papers)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Paper set operation failed: {exc}\n")
    print(f"{len(papers)} papers written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
