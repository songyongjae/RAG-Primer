from IPython.display import Markdown
import subprocess
import os

class get_primer:
    def __init__(self, subtitle, overview_content, finance_content, pie_chart_path, ticker):
        self.subtitle = subtitle
        self.overview_content = overview_content
        self.finance_content = finance_content
        self.pie_chart_path = pie_chart_path
        self.ticker = ticker

    def _markdown(self):
        # Generate Markdown content
        md = f"# {self.ticker.upper()} primer\n\n"
        md += f"**{self.subtitle}**\n\n"
        md += "## Overview\n"
        md += f'- {self.overview_content}' + "\n"

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
            metric_data = self.finance_content.get(metric, {})
            additional_data = self.finance_content.get(additional_key, {})
            md += f"| {metric}         | {metric_data.get('2021', 'N/A')} | {metric_data.get('2022', 'N/A')} | {metric_data.get('2023', 'N/A')} |\n"
            md += f"| *{additional_key}* | {additional_data.get('2021', 'N/A')}% | {additional_data.get('2022', 'N/A')}% | {additional_data.get('2023', 'N/A')}% |\n"

        if os.path.exists(self.pie_chart_path):
            md += f"\n## Segment Performance\n![Segment Performance Pie Chart]({self.pie_chart_path})\n"
        else:
            md += "\n(Segment Performance chart not available.)\n"
        Markdown(md)
        markdown_output_file = f'./{self.ticker}_primer_report.md'
        with open(markdown_output_file, 'w') as f:
            f.write(md)

    def _html_to_png_with_wkhtmltoimage(self, html_file, output_path):
        try:
            options = [
            '--enable-local-file-access',  # Allow local file access for embedded images
            '--format', 'png',
            '--width', '1240',  # Adjusted width for A4 (optimized for 96 DPI)
            '--height', '1300',  # Adjusted height for A4 (optimized for 96 DPI)
            '--crop-x', '0',  # Start cropping from the left edge
            '--crop-y', '0',  # Start cropping from the top edge
            '--crop-w', '1240',  # Crop width to match the page width
            '--crop-h', '1300',  # Crop height to match the page height
            '--disable-smart-width',  # Prevent automatic width adjustments
            '--quality', '100'  # High-quality output
            ]

            # Run the wkhtmltoimage command
            subprocess.run(
                ['wkhtmltoimage'] + options + [html_file, output_path],
                check=True
            )
            print(f"PNG successfully generated: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during image generation: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


    def generate_primer_png(self):
        self._markdown()
        try:
            # Generate Markdown content
            primer = f"<h1>{self.ticker.upper()} Primer</h1>\n"
            primer += "<h3>Overview</h3>\n"
            primer += f"<h2>{self.subtitle}</h2>\n"
            overview_lines = self.overview_content.split("\n")  # Assuming overview content has line breaks
            primer += "<ul>\n"  # Start an unordered list
            for line in overview_lines:
                primer += f"  <li>{line.strip()}</li>\n"  # Wrap each line in an <li> tag
            primer += "</ul>\n"  # End the unordered list

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
                metric_data = self.finance_content.get(metric, {})
                additional_data = self.finance_content.get(additional_key, {})
                primer += f"""
                <tr>
                    <td>{metric}</td>
                    <td>{metric_data.get('2021', 'N/A')}</td>
                    <td>{metric_data.get('2022', 'N/A')}</td>
                    <td>{metric_data.get('2023', 'N/A')}</td>
                </tr>
                <tr>
                    <td><i>{additional_key}</i></td>
                    <td>{additional_data.get('2021', 'N/A')}%</td>
                    <td>{additional_data.get('2022', 'N/A')}%</td>
                    <td>{additional_data.get('2023', 'N/A')}%</td>
                </tr>
                """
            primer += "</table>\n"

            if os.path.exists(self.pie_chart_path):
                primer += f"<h3>Segment Performance</h3>\n<img src='{self.pie_chart_path}' style='width: 100%;'>\n"
            else:
                primer += "<p>(Segment Performance chart not available.)</p>\n"

            # Save HTML content to a file
            html_file = f'./{self.ticker}_primer_report.html'
            with open(html_file, 'w') as f:
                f.write(primer)

            self._html_to_png_with_wkhtmltoimage(f'./{self.ticker}_primer_report.html', f'./{self.ticker}-primer-report.png')
        except Exception as e:
            print(f"An error occurred: {e}")