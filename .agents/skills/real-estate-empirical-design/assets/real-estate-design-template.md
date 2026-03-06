# Real Estate Design Template

## Asset and market
- **Economic object**: [property, borrower, lender, neighborhood, market, lease, REIT, developer]
- **Market segment**: [residential / commercial / multifamily / industrial / land]
- **Ownership type**: [owner-occupied, rental, institutional, REIT]

## Institutional setting
- **Key institution or policy**: [zoning rule, tax policy, lending regulation, insurance market, etc.]
- **Why this institution matters for the research question**:
- **Relevant institutional timeline**: [key dates, phase-ins, reforms]

## Geographic unit
- **Level of analysis**: [property, parcel, block, tract, ZIP, county, MSA, state]
- **Geographic scope**: [single city, state, multi-state, national]
- **Why this geography**: [variation source, data availability, external validity]

## Time variation
- **Sample period**: [start — end]
- **Treatment timing**: [single date, staggered, continuous]
- **Key temporal events in the market**: [booms, busts, policy changes within the sample]

## Main outcome
- **Primary outcome variable**: [price, rent, vacancy, default rate, permits, etc.]
- **Source**: [assessor, MLS, CoStar, HMDA, etc.]
- **Measurement concern**: [transaction vs. listing vs. appraised value; selection into observation]

## Main source of identification
- **Design type**: [hedonic, repeat-sales, boundary RD, spatial DiD, event study, hazard, other]
- **Source of variation**: [policy shock, regulatory boundary, natural disaster, market event, etc.]
- **Why this variation is informative**: [exogeneity argument]
- **Baseline specification**: [equation with notation]

## Spatial dependence plan
- **Expected spatial correlation structure**: [within-tract, within-ZIP, distance-based]
- **Standard error approach**: [Conley spatial HAC, cluster at geography, two-way cluster]
- **Justification for chosen approach**:

## Repeat observation handling
- **Are there repeat observations?** [yes/no]
- **If yes**: [how are they handled — property FE, repeat-sales differencing, panel structure]
- **Selection into repeat observation**: [are properties that transact multiple times representative?]

## Measurement-error concerns

| Variable | Concern | Remedy |
|---|---|---|
| [e.g., Property value] | [Appraisal smoothing] | [Use transaction data only] |
| [e.g., Property quality] | [Improvements between sales] | [Building permit data] |
| [e.g., Location] | [Geocoding error] | [Hand-audit sample, buffer zones] |

## Key institutional controls
- [List controls that are specific to the real estate setting and why they matter]
- [e.g., Property age, lot size, school quality, distance to CBD, zoning designation]

## Maps or visual aids needed
1. [e.g., Map showing treatment and control areas]
2. [e.g., Event-study plot around policy change]
3. [e.g., Spatial gradient of treatment effect by distance]
4. [e.g., Boundary-area detail map]

## Threats and remedies

| Threat | Severity | Diagnostic | Expected result |
|---|---|---|---|
| [e.g., Sorting across boundary] | [High/Med/Low] | [Balance test on observables] | [No discontinuity in covariates] |
| | | | |

## External validity assessment
- [Does this generalize beyond the specific geography/time period?]
- [What conditions would need to hold for the result to apply elsewhere?]
