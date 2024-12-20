import os
import re
import json
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def _construct_file_path(resources_dir, ticker, fiscal_year):
    """
    Constructs the file path for a given ticker and fiscal year.
    """
    return os.path.join(resources_dir, f"{ticker.lower()}-{fiscal_year}.html")

def _load_html(file_path):
    """
    Loads the HTML content of a file using LangChain's UnstructuredHTMLLoader.
    """
    return UnstructuredHTMLLoader(file_path).load()

def _extract_sections(html_content, section_titles, index_info):
    """
    Extracts sections from HTML content based on section titles.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n").strip()
    title_patterns = [re.escape(title) + r"(\s*continued)*" for title in section_titles]
    combined_pattern = re.compile(r"|".join(title_patterns), re.IGNORECASE)
    matches = list(combined_pattern.finditer(text))
    sections = {}
    for i, match in enumerate(matches):
        start_idx = match.start()
        end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = match.group(0)
        section_content = text[start_idx:end_idx].strip()
        if len(section_content.split()) > 5:
            sections[title] = section_content
    return sections

def _clean_sections(sections, index_info):
    """
    Cleans sections by removing overlapping text from subsequent section titles.
    """
    cleaned_sections = {}
    for section_title, content in sections.items():
        current_index = next((i for i, item in enumerate(index_info) if item.lower().startswith(section_title.lower())), None)
        if current_index is not None:
            next_section = index_info[current_index + 1] if current_index + 1 < len(index_info) else None
            if next_section:
                next_section_pattern = re.escape(next_section) + r"(\s*continued)*"
                next_section_match = re.search(next_section_pattern, content, re.IGNORECASE)
                if next_section_match:
                    content = content[:next_section_match.start()].strip()
            if content:
                cleaned_sections[section_title] = content
    return cleaned_sections

def _split_and_store_chunks(section_name, content, output_dir):
    """
    Splits a section's content into chunks and saves each chunk as a JSON file.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=150)
    chunks = splitter.split_text(content)
    for i, chunk in enumerate(chunks):
        output_file_path = os.path.join(output_dir, f"{section_name}_chunk_{i + 1}.json")
        with open(output_file_path, 'w') as json_file:
            json.dump({"chunk": chunk, "chunk_index": i + 1}, json_file, indent=4)
    return {"section": section_name, "chunk_count": len(chunks)}
