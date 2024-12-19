import openai
import json

def analyze_financials(documents, prompt_years):
    """
    Extract financial data for specific years using GPT.

    :param documents: List of JSON document data.
    :param prompt_years: List of years for which to extract data.
    :return: Parsed financial metrics as a dictionary.
    """
    all_content = "\n\n".join([doc.get('chunk', '') for doc in documents])

    if not all_content.strip():
        print("Error: No content provided to GPT for analysis.")
        return {}

    prompt = f"""
    You are a financial analyst. Based on the following content from chunks, extract financial metrics for the years {', '.join(prompt_years)}.
    - For ranges (e.g., "$8.00 to $10.00 billion"), calculate the average value.
    - If specific values for some years are missing, infer trends or use "N/A" if absolutely necessary.
    - Calculate YoY (Year-over-Year) percentage changes for Revenue.
    - Calculate margin percentages for Gross Profit, Operating Profit, and Net Profit where applicable.

    Instructions:
    1. Strictly return the output in JSON format.
    2. Do not include any additional explanations or commentary.
    3. Assume all dollar values are in billions unless stated otherwise.

    Filtered Content:
    {all_content}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert Financial assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        content = response['choices'][0]['message']['content'].strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON.")
            return {}
    except Exception as e:
        print(f"Unexpected GPT API error: {e}")
        return {}
