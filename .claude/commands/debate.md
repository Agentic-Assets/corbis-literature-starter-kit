---
description: Run a structured multi-round debate between two AI agents on a research question
---

Run a structured research debate on the following question:

$ARGUMENTS

Use the `research-debate` skill. Follow these steps:

1. Detect whether this is a single-claim (Skeptic vs Advocate), two-sided (Agent A vs Agent B), or evaluation (Optimist vs Critic) debate.
2. Calibrate round count: 2 rounds for simple binary choices, 3 rounds (default) for identification/method/contribution debates.
3. Check if the user referenced any project files and read them for context.
4. Run Round 1: launch both agents in parallel with their opening arguments.
5. Pause and ask if the user wants to inject information before Round 2.
6. Run remaining rounds, pausing between each unless the user asked to run uninterrupted.
7. Run the synthesis agent to produce the convergence report.
8. Save the report as DEBATE_[topic]_[date].md in the project root.
