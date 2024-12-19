from primer.file_reader import read_documents
from primer.content_combiner import combine_content
from primer.prompt_generator import generate_subtitle_prompt, generate_overview_prompt
from primer.openai_client import generate_response

def analyze_overview(folder_paths, filter_items):
    """
    Generate the subtitle and overview using text from the specified folder paths.

    :param folder_paths: List of folder paths to read JSON files.
    :param filter_items: List of keywords to filter JSON files.
    :return: Tuple of subtitle and overview text.
    """
    documents = read_documents(folder_paths, filter_items)
    combined_content = combine_content(documents)

    subtitle_prompt = generate_subtitle_prompt(combined_content)
    overview_prompt = generate_overview_prompt(combined_content)

    subtitle = generate_response(subtitle_prompt)
    overview_text = generate_response(overview_prompt)

    return subtitle, overview_text
