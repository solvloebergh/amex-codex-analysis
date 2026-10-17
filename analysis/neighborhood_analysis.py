#!/usr/bin/env python3
"""Summarize and chart unadjusted Ames sale prices by neighborhood."""
import csv
import html
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "AmesHousing-1.csv"
OUT = ROOT / "analysis"
SMALL_SAMPLE_CUTOFF = 10


def main():
    with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = reader.fieldnames or []
    if not {"Neighborhood", "SalePrice"}.issubset(fields):
        raise ValueError("CSV must contain Neighborhood and SalePrice columns")

    groups = defaultdict(list)
    label_counts = defaultdict(int)
    working_rows = []
    for row_number, row in enumerate(rows, start=2):
        raw_label = row["Neighborhood"]
        analysis_label = raw_label.strip()
        if not analysis_label:
            raise ValueError(f"Missing Neighborhood at CSV row {row_number}")
        try:
            price = float(row["SalePrice"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid SalePrice at CSV row {row_number}") from exc
        if price <= 0:
            raise ValueError(f"Nonpositive SalePrice at CSV row {row_number}")
        groups[analysis_label].append(price)
        label_counts[raw_label] += 1
        copy = dict(row)
        copy["Neighborhood_original"] = raw_label
        copy["Neighborhood_analysis"] = analysis_label
        copy["Neighborhood_changed"] = str(raw_label != analysis_label).lower()
        working_rows.append(copy)

    # This working copy explicitly records the raw and analysis labels. Trimming
    # is only a normalization rule; distinct resulting labels are never merged
    # by fuzzy matching or spelling assumptions.
    with (OUT / "neighborhood_working_copy.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields + ["Neighborhood_original", "Neighborhood_analysis", "Neighborhood_changed"])
        writer.writeheader()
        writer.writerows(working_rows)

    summary = []
    for neighborhood, prices in groups.items():
        summary.append({
            "neighborhood": neighborhood,
            "sale_count": len(prices),
            "median_sale_price": statistics.median(prices),
            "small_sample": len(prices) < SMALL_SAMPLE_CUTOFF,
        })
    summary.sort(key=lambda item: (item["median_sale_price"], item["neighborhood"]))
    with (OUT / "neighborhood_median_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["neighborhood", "sale_count", "median_sale_price", "small_sample"])
        writer.writeheader()
        for item in summary:
            writer.writerow({**item, "median_sale_price": f'{item["median_sale_price"]:.2f}'})

    # Generate a dependency-free, labeled SVG horizontal bar chart.
    width, margin_left, margin_right, row_height = 1050, 150, 180, 28
    top, bottom = 82, 92
    height = top + row_height * len(summary) + bottom
    axis_max = 350000
    plot_width = width - margin_left - margin_right
    axis_y = top + row_height * len(summary) + 5
    chart = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="white"/>',
             '<style>text{font-family:Arial,sans-serif;fill:#222}.title{font-size:20px;font-weight:bold}.small{font-size:12px}.label{font-size:13px}</style>',
             '<text x="24" y="30" class="title">Median Sale Price by Ames Neighborhood</text>',
             '<text x="24" y="51" class="small">Unadjusted medians; bar labels include sale counts. Small samples: fewer than 10 sales.</text>',
             f'<rect x="{width-310}" y="23" width="14" height="14" fill="#3569a8"/><text x="{width-290}" y="35" class="small">10 or more sales</text>',
             f'<rect x="{width-170}" y="23" width="14" height="14" fill="#d9822b"/><text x="{width-150}" y="35" class="small">Small sample</text>']
    for tick in range(0, axis_max + 1, 50000):
        x = margin_left + plot_width * tick / axis_max
        chart.append(f'<line x1="{x:.2f}" y1="{top-5}" x2="{x:.2f}" y2="{axis_y}" stroke="#dddddd" stroke-width="1"/>')
        chart.append(f'<text x="{x:.2f}" y="{axis_y+19}" text-anchor="middle" class="small">${tick:,.0f}</text>')
    chart.append(f'<line x1="{margin_left}" y1="{axis_y}" x2="{margin_left+plot_width}" y2="{axis_y}" stroke="#333" stroke-width="1.5"/>')
    for i, item in enumerate(summary):
        y = top + i * row_height
        bar_width = plot_width * item["median_sale_price"] / axis_max
        color = "#d9822b" if item["small_sample"] else "#3569a8"
        chart.append(f'<text x="{margin_left-10}" y="{y+16}" text-anchor="end" class="label">{html.escape(item["neighborhood"])}</text>')
        chart.append(f'<rect x="{margin_left}" y="{y}" width="{bar_width:.2f}" height="19" fill="{color}"/>')
        chart.append(f'<text x="{margin_left+bar_width+7:.2f}" y="{y+15}" class="small">${item["median_sale_price"]:,.0f} (n={item["sale_count"]})</text>')
    chart.append(f'<text x="{margin_left + plot_width/2:.1f}" y="{height-13}" text-anchor="middle" class="small">Median sale price (USD)</text>')
    chart.append('</svg>')
    (OUT / "neighborhood_median_chart.svg").write_text("\n".join(chart) + "\n", encoding="utf-8")

    total = sum(item["sale_count"] for item in summary)
    low, high = summary[0], summary[-1]
    narrative = (
        f"Across {total:,} analyzed sales in {len(summary)} neighborhoods, {high['neighborhood']} has the highest median sale price "
        f"(${high['median_sale_price']:,.2f}; {high['sale_count']} sales), while {low['neighborhood']} has the lowest "
        f"(${low['median_sale_price']:,.2f}; {low['sale_count']} sales). These are unadjusted neighborhood comparisons. "
        "House size, condition, and other factors have not been controlled for, so the differences should not be interpreted as neighborhood effects or causal findings."
    )
    (OUT / "findings.md").write_text("# Neighborhood median sale price findings\n\n" + narrative + "\n", encoding="utf-8")
    median_checks = ["# Independent median checks", "", "Sale prices below are sorted in ascending order within each neighborhood. For odd group sizes, the median is the single middle observation.", ""]
    for neighborhood in ("MeadowV", "StoneBr"):
        values = sorted(groups[neighborhood])
        middle_index = len(values) // 2
        median_checks += [f"## {neighborhood} (n={len(values)})", "", f"Median observation: position {middle_index + 1} of {len(values)} = ${values[middle_index]:,.2f}.", "", "Sorted SalePrice values (USD):", ""]
        median_checks.append(", ".join(f"${value:,.0f}" for value in values))
        median_checks.append("")
    (OUT / "extreme_median_check.md").write_text("\n".join(median_checks), encoding="utf-8")
    print(f"Analyzed records: {len(rows)}")
    print(f"Neighborhood sale counts sum: {total}")
    print(f"Neighborhood groups: {len(summary)}")
    print(f"Label whitespace changes: {sum(1 for row in working_rows if row['Neighborhood_changed'] == 'true')}")
    print(f"Lowest: {low['neighborhood']} | median=${low['median_sale_price']:.2f} | n={low['sale_count']}")
    print(f"Highest: {high['neighborhood']} | median=${high['median_sale_price']:.2f} | n={high['sale_count']}")


if __name__ == "__main__":
    main()
