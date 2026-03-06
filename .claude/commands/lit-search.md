---
description: Search the literature and build a positioning memo
---

Run the `literature-positioning-map` skill for the following topic or paper:

$ARGUMENTS

Execute the full mandatory search sequence:
1. Inner ring: `search_papers` for the exact question + method
2. Middle ring: same question with different methods, same method with different questions
3. Outer ring: `top_cited_articles` for seminal papers
4. Recent working papers: `internet_search` on SSRN and NBER
5. Verify close papers: `get_paper_details` on the top 5 results

Produce:
- Closest 3-5 papers with specific differentiation
- A draft contribution paragraph
- A related-literature outline
- BibTeX export of all cited papers via `export_citations`
