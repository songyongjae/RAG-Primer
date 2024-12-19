import os

def generate_markdown(subtitle, overview_content, finance_content, pie_chart_path, ticker):
    """
    Generate Markdown content for the financial primer.

    :param subtitle: Primer subtitle.
    :param overview_content: Overview text.
    :param finance_content: Financial data as a dictionary.
    :param pie_chart_path: Path to the pie chart image.
    :param ticker: Company ticker symbol.
    :return: Markdown content as a string.
    """
    md = f"# {ticker.upper()} Primer\n\n"
    md += f"**{subtitle}**\n\n"
    md += "## Overview\n"
    md += f"- {overview_content}\n\n"
    md += "## Financials\n"
    md += "| Metric($ million) | 2021   | 2022   | 2023   |\n"
    md += "|-------------------|--------|--------|--------|\n"

    metrics = [
        ("Revenue", "Revenue's % yoy"),
        ("Gross Profit", "Gross Profit's % margin"),
        ("Operating Profit", "Operating Profit's % margin"),
        ("Net Profit", "Net Profit's % margin")
    ]

    for metric, additional_key in metrics:
        metric_data = finance_content.get(metric, {})
        additional_data = finance_content.get(additional_key, {})
        md += f"| {metric}         | {metric_data.get('2021', 'N/A')} | {metric_data.get('2022', 'N/A')} | {metric_data.get('2023', 'N/A')} |\n"
        md += f"| *{additional_key}* | {additional_data.get('2021', 'N/A')}% | {additional_data.get('2022', 'N/A')}% | {additional_data.get('2023', 'N/A')}% |\n"

    if pie_chart_path and os.path.exists(pie_chart_path):
        md += f"\n## Segment Performance\n![Segment Performance Pie Chart]({pie_chart_path})\n"
    else:
        md += "\n(Segment Performance chart not available.)\n"

    return md
