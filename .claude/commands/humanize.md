---
description: Remove AI writing patterns from academic paper text
---

Run the `humanizer` skill on the following text or file:

$ARGUMENTS

Scan for AI writing patterns (significance inflation, promotional language, hollow mechanism language, mechanical table narration, em dashes, AI vocabulary, formulaic transitions, copula avoidance, synonym cycling, etc.) and rewrite to sound like a serious empirical researcher.

If given a file path (e.g., a `.tex` file), read the file and edit it in place. If given text in the prompt, return the revised version.

Preserve all citations, magnitudes, LaTeX commands, and substantive claims. Do not weaken the argument beyond what the patterns require.

After rewriting, do a referee-lens audit: "What would make a referee suspect this was AI-written?" Fix remaining tells.
