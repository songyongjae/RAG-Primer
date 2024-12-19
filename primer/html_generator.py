import os

def generate_html(markdown_content, ticker, pie_chart_path):
    """
    Generate an HTML version of the financial primer.

    :param markdown_content: Primer content in Markdown format.
    :param ticker: Company ticker symbol.
    :param pie_chart_path: Path to the pie chart image.
    :return: HTML content as a string.
    """
    primer = f"<h1>{ticker.upper()} Primer</h1>\n"
    primer += "<h3>Overview</h3>\n"
    primer += f"<h2>{markdown_content}</h2>\n"

    primer += "<h3>Financials</h3>\n"
    primer += """
    <table border="1" style="border-collapse: collapse; width: 100%; text-align: center;">
        <tr>
            <th>Metric($ million)</th>
            <th>2021</th>
            <th>2022</th>
            <th>2023</th>
        </tr>
    """

    metrics = [
        ("Revenue", "Revenue's % yoy"),
        ("Gross Profit", "Gross Profit's % margin"),
        ("Operating Profit", "Operating Profit's % margin"),
        ("Net Profit", "Net Profit's % margin")
    ]

    for metric, additional_key in metrics:
        primer += f"""
        <tr>
            <td>{metric}</td>
            <td>{markdown_content.get(metric, {}).get('2021', 'N/A')}</td>
            <td>{markdown_content.get(metric, {}).get('2022', 'N/A')}</td>
            <td>{markdown_content.get(metric, {}).get('2023', 'N/A')}</td>
        </tr>
        <tr>
            <td><i>{additional_key}</i></td>
            <td>{markdown_content.get(additional_key, {}).get('2021', 'N/A')}%</td>
            <td>{markdown_content.get(additional_key, {}).get('2022', 'N/A')}%</td>
            <td>{markdown_content.get(additional_key, {}).get('2023', 'N/A')}%</td>
        </tr>
        """
    primer += "</table>\n"

    if pie_chart_path and os.path.exists(pie_chart_path):
        primer += f"<h3>Segment Performance</h3>\n<img src='{pie_chart_path}' style='width: 100%;'>\n"
    else:
        primer += "<p>(Segment Performance chart not available.)</p>\n"

    return primer
