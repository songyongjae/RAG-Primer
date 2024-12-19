import os
import re
import json
import base64
import matplotlib.pyplot as plt
from langchain.docstore.document import Document
import openai
from pie_chart_analyzer.config import API_KEY

class get_pie_chart:
    """
    A class to analyze financial data from JSON documents, extract segment performance data,
    generate visualizations, and save the results in HTML format.
    """
    def __init__(self, api_key, legends, directory, ticker):
        """
        Initialize the SegmentAnalyzer with API key, legends, and the directory of JSON files.
        """
        openai.api_key = api_key
        self.legends = legends
        self.directory = directory
        self.ticker = ticker
        self.image_path = f"segment_performance_{self.ticker}.png"
        self.html_path = f"segment_performance_{self.ticker}.html"

    def load_json_files(self):
        """
        Load and preprocess JSON files from the directory.

        :return: List of Document objects with JSON content and metadata.
        """
        documents = []
        for filename in os.listdir(self.directory):
            if filename.endswith(".json"):
                with open(os.path.join(self.directory, filename), 'r') as file:
                    content = json.load(file)
                    documents.append(Document(page_content=json.dumps(content), metadata={"source": filename}))
        return documents

    def analyze_with_llm(self, documents):
        """
        Use OpenAI's GPT model to extract relevant content based on predefined legends.

        :param documents: List of Document objects.
        :return: Dictionary of segment performance data extracted by the LLM.
        """
        all_content = "\n\n".join([doc.page_content for doc in documents])
        prompt = f"""
You are a financial analyst. Based on the following content, extract revenue or percentage information for the following segments:
{', '.join(self.legends)}.

If no data exists for a segment, exclude it from your response. Format your response as JSON with each segment name as a key and its corresponding value as a number.

Content:
{all_content}
"""
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an expert Financial assistant."}, {"role": "user", "content": prompt}],
        )
        content = response['choices'][0]['message']['content'].strip()

        # Ensure the response is valid JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                raise ValueError("Response is not in JSON format.")

    def pie_chart_png(self, segment_data, output_path):
        """
        Generate a pie chart visualizing segment performance and save it as an image.
        """
        labels = list(segment_data.keys())
        sizes = list(segment_data.values())

        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct="%1.1f%%", startangle=140, textprops=dict(color="white")
        )
        ax.legend(wedges, labels, title="Segments", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=10, weight="bold")
        ax.set_title("Segment Performance")

        plt.savefig(output_path, format="png", bbox_inches="tight")
        plt.show()
        plt.close()
        print(f"Pie chart saved to {output_path}")

    def save_html_with_chart(self, image_path, html_path):
        """
        Embed the pie chart in an HTML file and save it.
        """
        with open(image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        html_snippet = f"""
        <html>
        <body>
            <h1>Segment Performance</h1>
            <img src="data:image/png;base64,{img_base64}" alt="Pie Chart">
        </body>
        </html>
        """

        with open(html_path, "w") as file:
            file.write(html_snippet)
        print(f"HTML file saved to {html_path}")

    def generate_pie_chart(self):
        """
        Perform the entire analysis workflow: load documents, analyze data, generate visualizations, and save results.
        """
        documents = self.load_json_files()
        if not documents:
            print("No JSON files found in the directory.")
            return

        try:
            segment_data = self.analyze_with_llm(documents)
            print("Segment data extracted:", segment_data)

            self.pie_chart_png(segment_data, self.image_path)
            self.save_html_with_chart(self.image_path, self.html_path)

        except Exception as e:
            print("Error:", e)
