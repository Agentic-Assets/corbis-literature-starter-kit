# Journal targeting guide for finance and real estate research

Last verified: 2026-03-06

## What this guide is for

This file is meant to help an LLM such as Claude Code advise researchers on:
- which journal is the best target for a paper
- how to reshape framing, contribution, methods, and robustness for that target
- what desk-reject signals to watch for
- what mutable submission details should be checked before submission

## Journal set used here

Finance core set:
- Journal of Finance
- Journal of Financial Economics
- Review of Financial Studies
- Journal of Financial and Quantitative Analysis
- Review of Finance

Real estate core set:
- Real Estate Economics
- Journal of Real Estate Finance and Economics
- Journal of Real Estate Research

Important adjacent outlets for housing and spatial real estate papers:
- Journal of Housing Economics
- Regional Science and Urban Economics

## How Claude should use this file

1. Classify the paper by its true contribution, not by the data source alone.
2. Score each candidate journal on:
   - broadness of contribution
   - topic fit
   - audience fit
   - method style
   - novelty level
   - real estate specificity
   - policy or business relevance
   - data and code readiness
3. Use hard filters first:
   - if the paper lacks a broad finance contribution, do not force it into JF, JFE, or RFS
   - if the paper is really urban or spatial economics, consider RSUE before specialty real estate journals
   - if the paper is really housing economics or housing policy, consider JHE before REE, JREFE, or JRER
4. Then use soft ranking:
   - JF, JFE, RFS: broad importance and first-order contribution
   - JFQA, Review of Finance: still top-tier finance, but often better when the contribution is somewhat more specialized, quantitative, or innovation-focused
   - REE: strongest broad real estate outlet
   - JREFE: finance and economics core
   - JRER: business and applied real estate core
5. When Claude recommends a target, it should also recommend concrete revisions that increase fit for that journal.


## Fast routing cheat sheet

### Finance papers
- Use **Journal of Finance** when the paper makes a first-order contribution with very broad finance importance.
- Use **Journal of Financial Economics** when the paper is tightly grounded in financial economics or the theory of the firm and has a strong mechanism or theory angle.
- Use **Review of Financial Studies** when the paper answers a major finance question with especially strong execution and broad implications.
- Use **Journal of Financial and Quantitative Analysis** when the paper is a strong finance paper with a sharper quantitative or specialized edge.
- Use **Review of Finance** when the paper has a crisp innovation story, including newer or cross-disciplinary finance topics.

### Real estate papers
- Use **Real Estate Economics** when the paper is one of the strongest broad real estate papers and has implications beyond a narrow local setting.
- Use **Journal of Real Estate Finance and Economics** when the paper is clearly framed through finance or economics, especially for mortgages, securitization, valuation, REITs, appraisals, and regulation.
- Use **Journal of Real Estate Research** when the paper has strong real estate business or decision relevance and should speak directly to a real estate audience.
- Use **Journal of Housing Economics** when the core question is housing economics, affordability, zoning, rental markets, demographics, or housing policy.
- Use **Regional Science and Urban Economics** when the real contribution is urban, spatial, regional, land-use, or infrastructure economics.


## Journal of Finance

**Status:** core top finance

**Official positioning:** Flagship American Finance Association journal. Broad generalist outlet for leading research across all major fields of financial research.

**Official scope:** Publishes leading research across all major fields of financial research. Official pages describe it as the most widely cited academic journal in finance.

**Current editors:**
- Antoinette Schoar (Editor)
- Leonid Kogan (Co-Editor)
- Jonathan Lewellen (Co-Editor)
- Thomas Philippon (Co-Editor)
- Adi Sunderam (Co-Editor)

**Submission logistics:**
- Submission fee: Fees vary by country income group and AFA membership. High-income economies: $400 for AFA members and $525 for nonmembers. Middle-income economies: $100 for members and $150 for nonmembers. Low-income economies: fee waived.
- Desk reject refund: High-income economy desk rejects receive a flat $200 refund.
- Slow decision policy: If a first-submission decision takes more than 100 days, the submission fee is refunded.
- Appeal fee: $600
- Reviewer credit: $250 submission-fee credit for timely referee reports.
- Open access: Subscription journal with open access option and self-archiving allowances for pre-publication versions.

**Transparency and research practices:** Has a substantially revised data and code policy. Accepted empirical or computational papers face data-editor review of the replication package. The journal also runs a Replications and Corrigenda section for short papers documenting material sensitivities or corrigenda.

**Recent topic examples:**
- Private meetings between asset managers and portfolio firms, using large language models to code meeting content
- Carbon pricing versus green finance
- Monetary policy, inflation, and crises
- Institutional investor attention
- Corporate ESG profiles and investor horizons
- Deposit insurance and depositor flows in failing banks

**Claude fit inference:** Best target when the paper makes a first-order contribution to finance rather than a narrow contribution to a single institutional setting. Claude should prefer JF when the draft changes how a broad finance audience thinks about an important mechanism, fact, or theory, and when the framing can be pitched to multiple finance subfields.

**Likely red flags:** Incremental extensions, mostly descriptive papers, papers with local or institutional interest but weak general importance, and papers with incomplete replication materials are likely poor fits.

**Development advice for Claude:**
- Push the introduction toward broad finance importance, not just setting-specific novelty.
- Force the paper to state the economic mechanism early and repeatedly.
- Ask whether the main result changes priors for researchers outside the immediate niche.
- Demand a clean replication package and explicit data-access discussion well before submission.
- Benchmark against recent JF-style topics only for breadth, not for mimicry.

**Official or near-official sources to verify:**
- Journal of Finance homepage and aims/scope (https://afajof.org/journal-of-finance/)
- Journal of Finance forthcoming articles (https://afajof.org/forthcoming-articles/)
- Journal of Finance editor and submission policy pages (https://afajof.org/)

## Journal of Financial Economics

**Status:** core top finance

**Official positioning:** Leading general finance journal with explicit emphasis on theoretical and empirical financial economics and the theory of the firm.

**Official scope:** Covers theoretical and empirical topics in financial economics and provides a specialized forum for work in financial economics and the theory of the firm.

**Current editors:**
- Toni Whited (Editor-in-Chief)
- Dimitris Papanikolaou (Co-Editor)
- Nikolai Roussanov (Co-Editor)
- Philipp Schnabl (Co-Editor)

**Submission logistics:**
- Submission fee: $850 for unsolicited new manuscripts.
- Desk reject refund: $400 refund on desk rejection, subject to limits related to prior rejections and repeated desk rejections.
- Slow decision policy: Submission fee refund if the first decision takes more than 120 days.
- Page charges: No page charges on the subscription route.
- Open access: Hybrid. Subscription route has no publication fee; open access APC listed as USD 5,210.
- Reported timeline: Publisher metrics report about 2 days from submission to first decision, 35 days from submission to decision after review, 536 days from submission to acceptance, and 17 days from acceptance to online publication.

**Transparency and research practices:** Very strong replication infrastructure. Accepted empirical, simulation, and experimental papers must provide data, code, and documentation through Mendeley Data or a domain repository. Restricted or proprietary data can use pseudo data plus detailed acquisition instructions. Code must cover data transformations and analysis steps, with software versions and random seeds where relevant. Experimental papers follow AER-style supplementary policies.

**Recent topic examples:**
- Misallocation and investment
- Life-cycle earnings dynamics, consumption, and portfolio choice
- Bank consolidation and pricing
- Public goods under financial distress
- Risk-free government debt manufacturing
- Social media as a bank-run catalyst
- The greenium
- Intermediation frictions in equity markets

**Claude fit inference:** Best target when the paper has a strong financial economics core and either a clear mechanism, a theory-heavy contribution, or a sharp empirical design with deep implications for firms, markets, or intermediation. Claude should route papers here when the argument is economically rich and technically tight, even if the framing is a bit more specialized than a classic JF pitch.

**Likely red flags:** Weakly motivated institution-only papers, descriptive results without mechanism, and manuscripts with shaky replication documentation are poor bets.

**Development advice for Claude:**
- Strengthen mechanism testing, not just average effects.
- Make the paper speak directly to a financial economics literature and, where relevant, the theory of the firm.
- If the paper uses proprietary or restricted data, explain replication strategy early.
- Expect very fast triage, so the cover letter and first two pages must make the contribution unmistakable.

**Official or near-official sources to verify:**
- ScienceDirect journal page (https://www.sciencedirect.com/journal/journal-of-financial-economics)
- Guide for authors (https://www.sciencedirect.com/journal/journal-of-financial-economics/publish/guide-for-authors)
- Volume 176, February 2026 (https://www.sciencedirect.com/journal/journal-of-financial-economics/vol/176/suppl/C)

## Review of Financial Studies

**Status:** core top finance

**Official positioning:** Society for Financial Studies flagship journal and one of the canonical top three general finance journals.

**Official scope:** Major forum for significant new research in financial economics. Official guidance emphasizes quality and importance to finance, interprets finance broadly including links to economics, and values both theoretical and empirical work.

**Current editors:**
- Tarun Ramadorai (Executive Editor)
- Viral Acharya (Editor)
- Andrey Malenko (Editor)
- Anna Pavlova (Editor)
- Clemens Sialm (Editor)
- David Sraer (Editor)
- Jessica Wachter (Editor)

**Submission logistics:**
- Submission fee: High-income economies: $400 for SFS members and $460 for nonmembers. Middle-income economies: $260 for members and $320 for nonmembers. Low-income economies: fee waived.
- Desk reject refund: $200 for high-income economies and $130 for middle-income economies.
- Appeal fee: $860
- Open access: Subscription journal with optional open access license after acceptance.

**Transparency and research practices:** Strong transparency and replication expectations. Accepted empirical, experimental, and computational papers must provide data, code, and documentation. A data editor reproduces core tables and figures inside a dedicated virtual environment. Synthetic or pseudo data can be used where direct data sharing is impossible.

**Policy signals:** The journal explicitly bars nontrivial recycling of rejected or under-review RFS papers without permission. It also requires manuscripts to be solely submitted and not previously published, including practitioner outlets.

**Recent topic examples:**
- Rationality and disagreement in house-price expectations
- Price and volume divergence in China’s real estate markets
- Agency MBS as safe assets
- Bank risk-taking and the real economy after the housing boom
- Inequality and the American debt boom
- Mortgage cramdown and household distress
- Intermediaries in real estate markets
- Option auctions and payment for order flow

**Claude fit inference:** Best target when the paper combines a major finance question with an especially clean empirical or theoretical execution and clear general-interest implications. Claude should treat RFS as hostile to purely applied, narrow, or practitioner-facing manuscripts unless the paper clearly speaks to a broad finance debate.

**Likely red flags:** Recycled variants of prior submissions, strongly practitioner-oriented work, narrow institutional notes, and papers whose general-interest hook appears only in the abstract are likely poor fits.

**Development advice for Claude:**
- Pressure test whether the question matters to a broad finance audience, not just the subfield.
- Highlight why the result changes theory, policy, or interpretation of prior evidence.
- Prepare the replication package as if it will be independently reproduced, because it may be.
- Avoid writing the paper like a consulting report or practitioner note.

**Official or near-official sources to verify:**
- Oxford Academic journal homepage (https://academic.oup.com/rfs)
- About the journal (https://academic.oup.com/rfs/pages/About)
- General instructions (https://academic.oup.com/rfs/pages/General_Instructions)
- Volume 39 Issue 2 (https://academic.oup.com/rfs/issue/39/2)

## Review of Finance

**Status:** high-end finance outlet

**Official positioning:** European Finance Association journal for high-quality and innovative work across financial economics.

**Official scope:** Welcomes high-quality papers in all areas of financial economics. Official policy emphasizes both quality and innovation, including established areas and newer fields such as law and finance, behavioral finance, and experimental finance.

**Current editors:**
- Marcin Kacperczyk (Managing Editor)

**Submission logistics:**
- Submission fee: €350 regular or resubmission fee, reduced to €300 for EFA members.
- Desk reject refund: €150 for non-EFA authors and €100 for EFA authors.
- Slow decision policy: Half of the submission fee is refunded if an editorial decision takes more than 120 days.
- Fast track: Fast-track option: €900 on first submission and €500 on resubmitted fast-track papers, with a 14-day editorial decision target.
- Formatting: 12-point font, 1.5 spacing, abstract no longer than 150 words.

**Transparency and research practices:** No unusually prominent journal-specific replication regime was foregrounded in the collected sources, so Claude should verify current data and code expectations on the OUP author pages before submission.

**Recent topic examples:**
- Special issue on biodiversity finance
- Corporate nature risk perceptions
- Biodiversity entrepreneurship
- Financial value of nature in coastal housing markets
- Biodiversity risk and local asset values

**Claude fit inference:** Best target when the paper is genuinely innovative, especially if it sits in a growing or cross-disciplinary area within finance. Claude should consider RoF for strong papers that may not be aimed at the very broadest North American generalist pitch but do have a crisp novelty story and broad academic interest.

**Likely red flags:** Incremental papers that feel like routine robustness extensions or minor follow-ons are poor fits because the journal's own policy language foregrounds innovation.

**Development advice for Claude:**
- Make novelty explicit in one sentence.
- When relevant, emphasize the paper's contribution to an emerging literature, not just to a narrow empirical setting.
- If speed matters and the paper is mature, consider whether fast-track review is strategically worthwhile.

**Official or near-official sources to verify:**
- Review of Finance general instructions (https://academic.oup.com/rof/pages/General_Instructions)
- Review of Finance 2026 issue archive (https://academic.oup.com/rof/issue-archive/2026)
- Volume 30 Issue 1 (https://academic.oup.com/rof/issue/30/1)

## Journal of Financial and Quantitative Analysis

**Status:** high-end finance outlet

**Official positioning:** Top finance journal with strong emphasis on financial economics and quantitative methods relevant to financial researchers.

**Official scope:** Publishes theoretical and empirical research in financial economics, including corporate finance, investments, capital and security markets, and quantitative methods.

**Current editors:**
- Hendrik Bessembinder (Managing Editor)
- Ran Duchin (Managing Editor)
- Thierry Foucault (Managing Editor)
- Jarrad Harford (Managing Editor)
- Kai Li (Managing Editor)
- George Pennacchi (Managing Editor)
- Stephan Siegel (Managing Editor)

**Submission logistics:**
- Submission fee: $350
- Desk reject refund: $275 refund if the managing editor does not send the paper to review.
- Submission volume: More than 1,000 manuscripts submitted annually; less than 9% printed.
- Formatting: 100-word abstract, 12-point Times New Roman, double-spaced main text and appendices.
- Dual submission: Partners with select conferences for dual submission without the initial JFQA submission fee.

**Transparency and research practices:** Code-sharing policy applies to new submissions from January 1, 2024 onward. Accepted empirical, simulation, or numerical papers must provide code needed to reproduce results from raw data. Authors must post code in the JFQA Harvard Dataverse. Raw data are required unless restricted by copyright or confidentiality, in which case pseudo data must be provided. Exceptions must be requested on initial submission.

**Recent topic examples:**
- Satellite data and unequal access to big data
- Political connections and tariff exemption grants
- Contrarian retail trading
- Price impact in auctions and continuous markets
- CRSP return changes and asset pricing
- Environmental consequences of anti-SLAPP laws

**Claude fit inference:** Best target when the paper is a strong finance manuscript with clear identification or theory and especially when the contribution is quantitative, methodologically sharp, or more specialized than a broad JF pitch. Claude should consider JFQA as a very strong home for rigorous capital markets, corporate finance, investments, and finance-methods papers.

**Likely red flags:** Papers without a clear financial economics contribution, papers that undersell their quantitative or methodological edge, and papers without a workable code-sharing plan are poor fits.

**Development advice for Claude:**
- Lean into the paper's methodological sharpness and design clarity.
- State exactly why the paper matters for financial researchers, not just for the institution or policy setting studied.
- Build the code and pseudo-data plan before the final round, not after conditional acceptance.

**Official or near-official sources to verify:**
- JFQA home (https://jfqa.org/)
- JFQA submissions (https://jfqa.org/submissions/)
- JFQA code sharing policy (https://jfqa.org/submissions/jfqa-code-sharing-policy/)
- Cambridge Core journal page (https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis)

## Real Estate Economics

**Status:** core top real estate

**Official positioning:** Official AREUEA journal and the field's premier general real estate outlet.

**Official scope:** Official pages describe REE as the premier journal on real estate topics. AREUEA describes it as the oldest academic journal focusing on real estate issues, first published in 1973, and as a journal that facilitates communication between researchers and industry professionals while improving the analysis of real estate decisions.

**Current editors:**
- Paul Carrillo
- Andra Ghent
- Andrew Hanson
- Alvin Murphy
- Eva Steiner

**Submission logistics:**
- Submission platform: Wiley Research Exchange for new submissions.
- Open access: Offers a Wiley open access option.
- Public fee disclosure: A public submission-fee schedule was not prominent in the collected official sources and should be verified directly before submission.

**Transparency and research practices:** The collected official pages emphasized scope and submission portal details more than replication mechanics. Claude should therefore verify any current data and code requirements directly on the Wiley author pages before submission.

**Editorial process signals:** AREUEA panel notes from editors suggest that the managing editor first performs an intake review, then assigns papers by subject expertise. The most common desk-reject reason mentioned in those notes is relevance or fit. The panel also highlighted novelty, a clearly stated contribution early in the paper, and citation of relevant REE work as practical signals of fit.

**Recent topic examples:**
- News media coverage and house-price predictability
- Explainable spatial machine learning for hedonic real estate models
- Natural disasters and housing prices
- Land-use deregulation and housing delivery
- Flood history and housing values
- Climate and real estate survey work

**Claude fit inference:** Best target for the strongest broad real estate papers, especially those with implications that extend beyond one local market. Claude should prioritize REE when the manuscript contributes to economics, finance, or policy through a real-estate setting and can be framed as relevant to the general real estate literature rather than only to a niche application.

**Likely red flags:** Weak field placement, failure to cite relevant REE work, local descriptive notes with limited generalization, and papers whose contribution is not obvious in the introduction are common fit risks.

**Development advice for Claude:**
- Make the contribution explicit in the first page.
- Show why the result matters for general real estate economics, not just for the local setting.
- Audit the reference list for REE placement and missing dialogue with the field.
- For climate, affordability, mobility, and urban change topics, stress why the paper advances a broader real estate question.

**Official or near-official sources to verify:**
- Wiley overview page (https://onlinelibrary.wiley.com/page/journal/15406229/homepage/productinformation.html)
- Wiley editorial board page (https://onlinelibrary.wiley.com/page/journal/15406229/homepage/editorialboard.html)
- AREUEA REE page (https://www.areuea.org/real-estate-economics)
- AREUEA WREN publishing panel notes (https://www.areuea.org/assets/PDFs_for_Articles/WREN%20Panel%20Notes%20062724%20Edited.pdf)
- Wiley author guidelines (https://onlinelibrary.wiley.com/page/journal/15406229/homepage/forauthors.html)

## Journal of Real Estate Finance and Economics

**Status:** core top real estate

**Official positioning:** Finance and economics oriented real estate journal with broad coverage spanning markets, institutions, mortgages, valuation, risk, and policy.

**Official scope:** Provides a forum for expanded theoretical and empirical research on real estate using the paradigms and methodologies of finance and economics. Coverage includes markets, institutional arrangements, mortgages and securitization, risk management and valuation, public policy and regulation, urban economics, housing, and regional science.

**Current editors:**
- Brent Ambrose (Editor-in-Chief)
- James Kau (Editor-in-Chief)
- Abdullah Yavas (Editor-in-Chief)
- R. Kelley Pace (Co-Editor)

**Submission logistics:**
- Submission platform: Springer online submission system.
- File requirements: Editable source files such as Word or LaTeX are required at every submission and revision stage.
- Open access: Hybrid. Reported APC: £2,490, $3,390, or €2,790. No APC on subscription route.
- Reported timeline: Publisher page reports a median of 4 days from submission to first decision.
- Downloads: Publisher reports about 269.5k downloads in 2025.

**Transparency and research practices:** The collected sources emphasized scope, editorial structure, and logistics more than a journal-specific data archive regime. Claude should verify current transparency requirements on Springer author pages before final submission.

**Practical editorial signals:** AREUEA panel notes suggest an initial desk screen for field fit, consulting-report style, and clarity of writing. The same notes stress relevance to the field and visible placement in the real estate literature.

**Recent topic examples:**
- Crime and housing prices with quantile and spatial methods
- Uncertainty quantification in automated valuation models
- Explainable AI for automated valuation
- Racial disparity in appraisals
- House-search traffic
- REIT returns and volatility with explainable machine learning
- Monetary policy and REITs
- REIT bond risk premia
- Option markets for REITs

**Claude fit inference:** Best target when the real-estate paper is unmistakably grounded in finance or economics. Claude should route here for mortgage, securitization, valuation, REIT, appraisal, risk-management, institutional, and regulation papers, as well as housing or urban papers whose main value added is real-estate finance or economics rather than policy alone.

**Likely red flags:** Papers that read like industry consulting reports, have unclear writing, lack a finance/economics backbone, or are weakly connected to the real estate literature are poor fits.

**Development advice for Claude:**
- Tell the editor exactly which finance or economics mechanism is being tested.
- Make the paper legible to both real estate and mainstream economics readers.
- If using ML or AVM methods, connect prediction gains to valuation, risk, or market design rather than only to model accuracy.

**Official or near-official sources to verify:**
- Springer journal page (https://link.springer.com/journal/11146)
- Volumes and issues (https://link.springer.com/journal/11146/volumes-and-issues)
- Volume 72 Issue 3 (https://link.springer.com/journal/11146/volumes-and-issues/72-3)
- Volume 72 Issue 1 (https://link.springer.com/journal/11146/volumes-and-issues/72-1)
- AREUEA WREN publishing panel notes (https://www.areuea.org/assets/PDFs_for_Articles/WREN%20Panel%20Notes%20062724%20Edited.pdf)

## Journal of Real Estate Research

**Status:** core top real estate

**Official positioning:** Flagship American Real Estate Society journal with broad business-facing real estate coverage.

**Official scope:** Official snippets describe JRER as covering housing, development, economics, finance, investment, law, management, marketing, secondary markets, and valuation. The journal states that its objective is to investigate and expand the frontiers of knowledge covering business applications through scholarly real estate research.

**Current editors:**
- Michael J. Seiler (Co-Editor)
- Zhenguo Lin (Co-Editor)

**Submission logistics:**
- Submission platform: ARES electronic review system.
- Open access: Taylor & Francis Open Select is available.
- Public fee disclosure: A current public submission-fee schedule was not confirmed in the collected official sources.

**Transparency and research practices:** The accessible official snippets focused on scope and submission access rather than an explicit journal-specific data archive policy. Claude should verify current transparency requirements on the Taylor & Francis author pages before submission.

**Editorial signal:** The Taylor & Francis about-page snippet says the editorial board is interested in broadening the reach of scholarly real estate research and is willing to work with potential authors who carefully develop the manuscript.

**Recent topic examples:**
- Behavioral responses to nominal property-tax changes using self-assessed home values in U.S. counties

**Claude fit inference:** Best target when the manuscript has clear real estate business or decision-making relevance and a recognizable real-estate audience, but does not necessarily need the broadest economics or finance framing of REE. Claude should consider JRER for solid real estate finance, valuation, taxation, management, brokerage, secondary-market, and applied market-behavior papers.

**Likely red flags:** Papers with weak real-estate decision relevance, papers that never explain why the result matters to real estate professionals or firms, and papers framed as pure abstract theory with little business application are weaker fits.

**Development advice for Claude:**
- Translate technical results into implications for real-estate decisions, markets, or institutions.
- Keep the literature review strongly anchored in real-estate scholarship, not just general economics.
- If the paper is more practice-oriented than REE or JREFE, JRER may be the better target.

**Official or near-official sources to verify:**
- ARES JRER page (https://www.aresnet.org/page/JRER)
- Taylor & Francis journal page (https://www.tandfonline.com/journals/rjer20)
- Taylor & Francis about page (https://www.tandfonline.com/journals/rjer20/about-this-journal)
- Taylor & Francis latest articles (https://www.tandfonline.com/action/showAxaArticles?journalCode=rjer20)

## Journal of Housing Economics

**Status:** adjacent housing/real estate outlet

**Official positioning:** Important economics outlet for housing research, especially housing policy, affordability, regulation, and spatial housing questions.

**Official scope:** Provides a focal point for economic research related to housing and explicitly encourages careful analytical technique on important housing-related questions. Topics include housing markets, public policy, real estate, finance, spatial models, demographics and mobility, and law and regulation.

**Current editors:**
- N.E. Coulson (Editor)
- O. Pollakowski (Editor)
- D.A. Hartley (Co-Editor)
- J.E. Zabel (Co-Editor)

**Submission logistics:**
- Submission fee: $100 for regular submissions and $25 for students.
- Peer review: Single anonymized peer review. Editors first assess suitability, then usually send suitable papers to at least two reviewers.
- Appeals: One appeal per submission.
- Desk reject policy: Editors may desk reject papers that are inconsistent with aims, scope, or style.
- Open access: Subscription route has no publication fee; reported open access APC is USD 3,530.
- Reported timeline: Publisher page reports about 9 days from submission to first decision, 76 days to decision after review, 282 days to acceptance, and 9 days from acceptance to online publication.

**Transparency and research practices:** Guide for authors requires a data-availability statement at submission.

**Recent topic examples:**
- Coastal hazards and housing redevelopment
- Low-income housing programs and recipient wellbeing
- Shelter inflation and the new-tenant versus all-tenant rent gap
- Upzoning special issue
- Local public finance and housing special issue

**Claude fit inference:** Best target when the central contribution is housing economics rather than general finance or real estate business practice. Claude should route here for affordability, zoning, rental markets, housing policy, housing finance with household or policy emphasis, demographic mobility, and regulatory questions.

**Likely red flags:** Papers that are mostly about REIT pricing, commercial real estate capital markets, or broad finance questions without a central housing contribution are weaker fits.

**Development advice for Claude:**
- Stress the housing question first and the econometrics second.
- Tie the contribution to public policy or a major housing mechanism where possible.
- Use the introduction to show why the result matters for housing economics rather than for finance broadly.

**Official or near-official sources to verify:**
- ScienceDirect journal page (https://www.sciencedirect.com/journal/journal-of-housing-economics)
- Guide for authors (https://www.sciencedirect.com/journal/journal-of-housing-economics/publish/guide-for-authors)
- Articles in press (https://www.sciencedirect.com/journal/journal-of-housing-economics/articles-in-press)
- Special issues (https://www.sciencedirect.com/journal/journal-of-housing-economics/special-issues)

## Regional Science and Urban Economics

**Status:** adjacent urban/spatial outlet

**Official positioning:** High-value outlet for urban, spatial, and regional economics. Often a strong home for housing and land-use papers that are really urban or regional economics papers.

**Official scope:** Encourages high-quality scholarship on important issues in regional and urban economics. Papers may be theoretical or empirical, positive or normative, but they must have a clear spatial dimension. Empirical papers studying causal mechanisms are expected to propose a convincing identification strategy.

**Current editors:**
- Gabriel Ahlfeldt (Editor)
- Laurent Gobillon (Editor)

**Submission logistics:**
- Submission fee: $100 for regular manuscripts and $50 for full-time students.
- Page charges: No page charges.
- Open access: Subscription route has no publication fee; reported open access APC is USD 3,830.

**Transparency and research practices:** The official guide foregrounds identification standards for empirical work and the journal's spatial dimension requirement.

**Recent topic examples:**
- Roads, transit, and urbanization in São Paulo
- Birth dearth and local population decline
- Tourism and urban revival
- Rail disinvestment and spatial impacts

**Claude fit inference:** Best target when the paper's real contribution is urban, regional, or spatial economics, even if the application uses housing or real estate data. Claude should prefer RSUE over real-estate specialty journals when the model, identification, and claims are really about cities, land use, migration, infrastructure, neighborhood change, or spatial equilibrium.

**Likely red flags:** Pure real estate finance papers, valuation-only papers, or manuscripts with weak identification and little spatial economics content are poor fits.

**Development advice for Claude:**
- Lead with the spatial mechanism and identification strategy.
- Explain why the result matters for urban or regional economics, not merely for a property market.
- If the data are real estate but the theory is spatial, RSUE may dominate specialty real-estate outlets.

**Official or near-official sources to verify:**
- ScienceDirect journal page (https://www.sciencedirect.com/journal/regional-science-and-urban-economics)
- Guide for authors (https://www.sciencedirect.com/journal/regional-science-and-urban-economics/publish/guide-for-authors)
- Journal insights (https://www.sciencedirect.com/journal/regional-science-and-urban-economics/about/insights)
- All issues (https://www.sciencedirect.com/journal/regional-science-and-urban-economics/issues)