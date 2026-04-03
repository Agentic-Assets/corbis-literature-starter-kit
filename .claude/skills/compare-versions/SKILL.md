---
name: compare-versions
description: Show diff between current and proposed text with change rationale
user_invocable: true
---

# Compare Versions Skill

Show a side-by-side comparison of old vs. new text after an edit, with rationale for each change.

## Examples
- `/compare-versions` -- compare after the most recent edit
- `/compare-versions introduction` -- compare current vs. proposed introduction text

## Workflow

1. Identify the two text versions (before and after edit)
2. Align paragraphs between versions
3. For each changed paragraph, show:
   - **Before**: The original text
   - **After**: The revised text
   - **Why**: Category of change (banned word, terminology, voice, precision, concision, restructure)
4. Summarize total changes by category

## Output Format

```
COMPARISON: [section name]
==========================

CHANGE 1 [Banned word]:
  Before: "...we utilize a comprehensive set of..."
  After:  "...we use a thorough set of..."

CHANGE 2 [Terminology]:
  Before: "...microstructure noise affects..."
  After:  "...measurement error affects..."

[etc.]

SUMMARY:
- Banned words fixed: N
- Terminology corrections: N
- Voice improvements: N
- Precision additions: N
- Concision cuts: N
- Total changes: N
```
