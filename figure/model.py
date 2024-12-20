import os
from utils import load_json_files, analyze_with_llm, generate_pie_chart, save_html_with_chart

class get_pie_chart:
    def __init__(self, api_key, legends, directory, ticker):
        self.api_key = api_key
        self.legends = legends
        self.directory = directory
        self.ticker = ticker
        self.image_path = f"figure/segment_performance_{self.ticker}.png"
        self.html_path = f"figure/segment_performance_{self.ticker}.html"

    def generate_pie_chart(self):
        """
        Perform the entire analysis workflow: load documents, analyze data, generate visualizations, and save results.
        """
        # Load JSON documents
        documents = load_json_files(self.directory)
        if not documents:
            print("No JSON files found in the directory.")
            return

        # Analyze using LLM
        try:
            segment_data = analyze_with_llm(self.api_key, self.legends, documents)
            print("Segment data extracted:", segment_data)

            # Generate pie chart
            generate_pie_chart(segment_data, self.image_path)

            # Save HTML with chart
            save_html_with_chart(self.image_path, self.html_path)

        except Exception as e:
            print("Error during chart generation:", e)
