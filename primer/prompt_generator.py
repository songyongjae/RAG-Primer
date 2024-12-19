def generate_subtitle_prompt(content):
    """
    Generates a prompt for creating the subtitle.

    :param content: Combined content from JSON files.
    :return: Subtitle generation prompt.
    """
    return f"""
    Based on the following content about a company, create a short one-line subtitle (10 words or fewer)
    that describes the company's identity (e.g., "vehicle manufacturer") and specialties
    (e.g., "renewable energy solutions" or "solar energy systems").

    Content:
    {content}
    """

def generate_overview_prompt(content):
    """
    Generates a prompt for creating the overview paragraph.

    :param content: Combined content from JSON files.
    :return: Overview generation prompt.
    """
    return f"""
    You are a financial analyst. Based on the following content, summarize the company in a concise paragraph of 5 sentences or less.
    The paragraph should:
    1. Start with a one-liner explaining the company's identity and specialties.
    2. Describe how the company generates revenue, who they sell to, and the distribution of sales across their customer base.
    3. Provide key context about their business model. This is most important.

    Content:
    {content}
    """
