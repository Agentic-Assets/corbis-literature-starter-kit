# Citation Verification Protocol

NEVER write a \cite{} command or BibTeX entry without verification. No exceptions.

## When citing an existing key
1. Confirm KEY exists in the project's `.bib` file
2. Verify the BibTeX entry matches the claim being made (correct author, year, topic)

## When citing a new paper
1. Search the `.bib` file for an existing entry (by author, year, or title keywords)
2. If not found: use `search_papers` (Corbis MCP) to verify the paper exists
   - Query: "{Author} {Year} {key title words}" academic paper
   - Confirm: exact title, all author names, publication year, journal/venue
   - Use `get_paper_details` (Corbis MCP) for full metadata when available
3. If confirmed: generate BibTeX entry, offer to append to the `.bib` file
4. If NOT confirmed: do NOT cite. Write the argument without the citation.
   State: "Could not verify this reference via web search."

## When you think of a paper from memory
STOP. Do NOT trust training data for author names, years, or titles.
Common failure modes: wrong year (off by 1-2), wrong co-author, confused with similar paper.
Always follow the "citing a new paper" workflow above.

## When writing economic arguments
Proactively search for supporting references using `search_papers` and `get_paper_details` (Corbis MCP tools).
This strengthens the writing AND ensures citations are real.

## Field-by-field verification (CRITICAL)
When verifying ANY citation — new or existing — compare EACH BibTeX field against search results:
- **Authors**: every author name must appear in search results
- **Title**: exact title must appear in search results
- **Year**: must match search results exactly
- **Journal**: must be explicitly named in search results (not inferred from memory)
- **Volume/Pages**: only report if explicitly found in search results

**The golden rule**: If a field (especially journal, volume, or pages) does NOT appear in search results, report it as `UNCONFIRMED` — NEVER fill it in from training data. This is the #1 source of hallucinated citation metadata.

**Forthcoming / working papers**: These are especially dangerous. Search results often show NBER/SSRN versions without journal placement. If you cannot find explicit confirmation of the journal name in search results, say: "Journal: UNCONFIRMED (not found in search results; BibTeX says {X})".

## BibTeX conventions
- Multi-author keys: Author1-Author2-Year (e.g., Fama-French-1993)
- Single-author keys: authorYYYYword (e.g., cochrane2005writing)
- @article for published, @misc/@unpublished for working papers
- Protect proper nouns in titles with braces: {TRACE}, {U.S.}, {NYSE}

## What NOT to do
- Do NOT invent plausible-sounding citations
- Do NOT generate BibTeX from memory alone
- Do NOT assume a paper exists because the topic + author seems right
- Do NOT cite retracted papers without flagging the retraction
- Do NOT fill in journal, volume, or pages from memory when search results don't mention them
- Do NOT report a citation as "OK" unless EVERY field has been independently confirmed
