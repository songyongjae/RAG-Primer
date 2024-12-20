import os
import re
import json
import base64
import openai
import matplotlib.pyplot as plt

def load_json_files(directory):
    """
    Load and preprocess JSON files from the directory.

    :param directory: Directory containing JSON files.
    :return: List of dictionaries with JSON content.
    """
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r') as file:
                content = json.load(file)
                documents.append({"content": content, "metadata": {"source": filename}})
    return documents

def analyze_with_llm(api_key, legends, documents):
    """
    Use OpenAI's GPT model to extract relevant content based on predefined legends.

    :param api_key: OpenAI API key.
    :param legends: List of financial segments to extract.
    :param documents: List of dictionaries with JSON content.
    :return: Dictionary of segment performance data extracted by the LLM.
    """
    openai.api_key = api_key
    all_content = "\n\n".join([json.dumps(doc["content"]) for doc in documents])
    prompt = f"""
You are a financial analyst. Based on the following content, extract revenue or percentage information for the following segments:
{', '.join(legends)}.

If no data exists for a segment, exclude it from your response. Format your response as JSON with each segment name as a key and its corresponding value as a number.

Content:
{all_content}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an expert Financial assistant."}, {"role": "user", "content": prompt}],
    )
    content = response['choices'][0]['message']['content'].strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("Response is not in JSON format.")

def generate_pie_chart(segment_data, output_path):
    """
    Generate a pie chart visualizing segment performance and save it as an image.

    :param segment_data: Dictionary of segment data to visualize.
    :param output_path: Path to save the pie chart image.
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
    plt.close()

def save_html_with_chart(image_path, html_path):
    """
    Embed the pie chart in an HTML file and save it.

    :param image_path: Path to the pie chart image.
    :param html_path: Path to save the HTML file.
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
