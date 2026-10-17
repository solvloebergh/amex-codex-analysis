# How does median sale price vary across neighborhoods in Ames, and which neighborhoods have the highest and lowest median prices?

Session date: 2026-10-17

## Findings

Across 2,930 analyzed sales in 28 neighborhoods, StoneBr has the highest median sale price ($319,000, 51 sales), 
while MeadowV has the lowest ($88,250, 37 sales). 
Neighborhoods with fewer than 10 sales are flagged as small samples and remain included; 
the chart and summary table show sale counts for every neighborhood.

These are unadjusted comparisons. House size, condition, and other factors have not been controlled for, 
so the differences should not be interpreted as neighborhood effects or causal findings.

### Reproduce the analysis

From the repository root, run:

```sh
python3 analysis/neighborhood_analysis.py
```

The script uses Python's standard library and reads `AmesHousing-1.csv` without modifying it. It writes the auditable working copy, median summary table, SVG chart, and findings narrative under `analysis/`.

- [Neighborhood summary CSV](analysis/neighborhood_median_summary.csv)
- [Median price chart](analysis/neighborhood_median_chart.svg)
- [Sorted values for independent median checks](analysis/extreme_median_check.md)
- [Findings narrative](analysis/findings.md)
- [Analysis script](analysis/neighborhood_analysis.py)
