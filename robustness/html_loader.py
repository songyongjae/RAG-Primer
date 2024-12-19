import os
from langchain.document_loaders import UnstructuredHTMLLoader

def load_html_file(file_path):
    """
    Loads an HTML file and returns its text content.

    :param file_path: Path to the HTML file.
    :return: Text content of the HTML document.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")

    document = UnstructuredHTMLLoader(file_path).load()[0]
    return document.page_content
