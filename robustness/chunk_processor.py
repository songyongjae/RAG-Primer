import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_section(ticker, fiscal_year, section_name, content, output_dir):
    """
    Splits a document section into chunks and saves them as JSON files.

    :param ticker: Company ticker symbol.
    :param fiscal_year: Fiscal year of the document.
    :param section_name: Name of the section.
    :param content: Section content to split.
    :param output_dir: Directory to save the chunks.
    :return: Dictionary with chunk metadata.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=150)
    chunks = splitter.split_text(content)
    chunk_files = []

    for i, chunk in enumerate(chunks):
        output_file_path = os.path.join(output_dir, f"{section_name}_chunk_{i + 1}.json")
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump({"chunk": chunk, "chunk_index": i + 1}, json_file, indent=4)
        chunk_files.append(output_file_path)

    return {"section": section_name, "chunk_count": len(chunks), "chunk_files": chunk_files}
