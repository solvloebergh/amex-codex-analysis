# AI Workflow Log

## Entry 1: Initial dataset inspection

- **Prompt file:** `prompts/01-initial-inspection.txt`
- **Local timestamp:** 2026-10-17 14:47:02 EDT (UTC-04:00)
- **Work produced:** Read-only inspection of `AmesHousing-1.csv`; repository README updated with the analytical question, session date, and pending findings; initial prompt saved verbatim; this workflow log created. The initial pandas attempt failed because pandas was not installed; the built-in Python `csv` fallback completed the inspection.
- **Inspection results:** 2,930 rows × 82 columns. Relevant columns: `Neighborhood`, `SalePrice`. Missing values: 0 in each. Exact duplicate records beyond the first: 0. SalePrice values: 2,930 positive numeric; 0 missing, 0 nonnumeric, and 0 nonpositive numeric.
- **Cleaning plan (recommendation):** Keep the source CSV unchanged. For analysis, work on a separate in-memory or derived copy, confirm the two fields have expected types, trim and inspect neighborhood labels for inconsistent spelling/spacing, and retain only valid positive numeric sale prices with nonmissing neighborhoods if any issues are found. Since the initial checks found no missing/invalid values or exact duplicate rows, do not remove records without a documented reason.
- **Simple analysis plan (recommendation):** Group valid sales by `Neighborhood`; compute median `SalePrice` and sale count for each group; sort by median sale price to identify the highest- and lowest-median neighborhoods; present a concise table and a sorted bar chart if useful. Do not interpret small group differences without considering neighborhood sample sizes.
- **Student acceptance:** Accepted keeping all 2,930 records because no missing `Neighborhood` or invalid `SalePrice` values or exact duplicate rows were found; accepted median comparison refined to include sale counts, flag samples under 10 without excluding them, and describe results as unadjusted comparisons.
- **Student modifications:** Add a sale count for every neighborhood; flag neighborhoods with fewer than 10 sales as small samples while retaining them; use unadjusted, noncausal language.
- **Student rejections:** None stated.

## Entry 2: Neighborhood median analysis

- **Prompt file:** `prompts/02-neighborhood-analysis.txt`
- **Local timestamp:** 2026-10-17 14:54:12 EDT (UTC-04:00)
- **Work produced:** Created `analysis/neighborhood_analysis.py`, an auditable working copy, a sorted neighborhood summary CSV, a labeled SVG horizontal bar chart, a findings narrative, and README reproduction instructions. The script uses Python's standard library; no package installation was required.
- **Label review:** 28 raw neighborhood labels; none had leading or trailing whitespace. The working copy records original and analysis labels and a changed flag. No labels were changed or merged. Potential spelling differences were not inferred or silently merged.
- **Results:** 2,930 records across 28 neighborhoods. Highest median: StoneBr, $319,000, 51 sales. Lowest median: MeadowV, $88,250, 37 sales. Groups with fewer than 10 sales are flagged and retained. Comparisons are described as unadjusted; house size, condition, and other factors are uncontrolled.
- **Verification:** Script grouped-count sum = 2,930, matching the 2,930 analyzed records. An independent standard-library recalculation from the source CSV also gave a grouped-count sum of 2,930, MeadowV median $88,250 (n=37), and StoneBr median $319,000 (n=51).
- **Student acceptance of new outputs:** Accepted the neighborhood summary table and findings for the stated descriptive question, based on the documented checks and assisted review. The requested chart-axis modification is complete.
- **Student modifications to new outputs:** None; student stated there are no further modifications.
- **Student rejections of new outputs:** None; student stated there are no rejections.

## Entry 3: Chart review and median verification

- **Prompt file:** `prompts/03-chart-review.txt`
- **Local timestamp:** 2026-10-17 15:00:01 EDT (UTC-04:00)
- **Student review of existing chart:** Student reviewed the labels, ordering, sale counts, and small-sample colors and requested that these elements be retained.
- **Requested changes:** Add a zero-based horizontal axis labeled `Median sale price (USD)` with readable currency ticks; verify all 28 plotted values and counts against the summary CSV; show sorted `SalePrice` values and the middle median observation for MeadowV and StoneBr.
- **Work produced:** Updated the standard-library script and regenerated the chart with ticks from $0 to $350,000 in $50,000 steps. Created `analysis/extreme_median_check.md` with all sorted values and median positions. Added a README link to that verification note.
- **Chart-to-summary verification:** Parsed the SVG and CSV independently: 28 labels and 28 value/count annotations were present, and every label, value, and count matched the summary CSV in the same order. The axis label and $0 tick were also confirmed.
- **Median verification data:** MeadowV has 37 sorted values; position 19 is $88,250. StoneBr has 51 sorted values; position 26 is $319,000.
- **Acceptance of revised chart:** Accepted by student after opening and reviewing it. Retain the zero-based currency axis, neighborhood labels, sale counts, ordering, and small-sample colors.
- **Median check status:** Resolved with ChatGPT assistance; do not characterize as an independent manual verification by the student. Student confirmed MeadowV position 19 of 37 = $88,250 and StoneBr position 26 of 51 = $319,000.

## Entry 4: Review decisions

- **Prompt file:** `prompts/04-review-decisions.txt`
- **Local timestamp:** 2026-10-17 15:05:52 EDT (UTC-04:00)
- **Student decisions recorded:** Accepted the revised chart after opening and reviewing it, retaining the zero-based currency axis, neighborhood labels, sale counts, ordering, and small-sample colors. Confirmed the MeadowV and StoneBr median positions and values with ChatGPT assistance; this is not recorded as an independent manual verification.
- **Work produced:** Saved this prompt verbatim and updated the prior chart-review log entry to resolve chart acceptance and median-check status.
- **Other review decisions:** None stated.

## Entry 5: Reflection

- **Prompt file:** `prompts/05-reflection.txt`
- **Local timestamp:** 2026-10-17 15:09:58 EDT (UTC-04:00)
- **Work produced:** Created `reflection.md` using the student's stated reflections and documented session examples. It notes the separate ChatGPT conversation for step-by-step guidance and prompt drafting, and that analytical work was executed in Codex CLI using the student's Clemson Edu account. It does not claim the student wrote the code or understood every command.
- **Review of reflection:** Accepted by student after the chart-review sentence was corrected to state that the first chart was missing a horizontal price axis; see Entry 7.

## Entry 6: Reflection wording revision

- **Prompt file:** `prompts/06-reflection-revision.txt`
- **Local timestamp:** 2026-10-17 15:12:23 EDT (UTC-04:00)
- **Work produced:** Replaced only the ChatGPT-assistance statement in `reflection.md` with the requested wording. Earlier prompt files and the rest of the reflection remain unchanged.
- **Review of revised reflection:** Accepted by student after the chart-review sentence was corrected to state that the first chart was missing a horizontal price axis; see Entry 7.

## Entry 7: Final reflection review and repository audit

- **Prompt file:** `prompts/07-final-review.txt`
- **Local timestamp:** 2026-10-17 15:22:58 EDT (UTC-04:00)
- **Student decision:** Accepted `reflection.md` after correcting the chart-review sentence to state that the first chart was missing a horizontal price axis.
- **Work produced:** Corrected that sentence, saved this prompt, and audited the requested repository artifacts, pending review items, and source CSV status.
- **Review of corrected reflection:** Accepted by student.

## Entry 8: Analysis-output acceptance

- **Prompt file:** `prompts/08-analysis-acceptance.txt`
- **Local timestamp:** 2026-10-17 15:27:16 EDT (UTC-04:00)
- **Student decision:** Accepted the neighborhood summary table and findings for the stated descriptive question, based on documented checks and assisted review. The chart-axis modification is complete. No further modifications or rejections were stated.
- **Work produced:** Updated the three analysis-output review fields in Entry 2 and saved this prompt. Earlier prompt history was preserved.
- **Analysis and reflection:** Unchanged.
