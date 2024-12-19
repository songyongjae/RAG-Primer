import os
import re
import json
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import shutil
from html_section_processor.config import DATASET_DIR, ITEMS, INDEX_INFO

class get_sources_10k:
    """
    A class for processing 10-K HTML documents and extracting, cleaning, and chunking sections.
    """

    def __init__(self):
        self.resources_dir = DATASET_DIR
        self.metadata = {}  # Metadata dictionary for processed files
        self.items = ITEMS
        self.index_info = INDEX_INFO

    def _construct_file_path(self, ticker, fiscal_year):
        """
        Constructs the file path for a given ticker and fiscal year.
        """
        return os.path.join(self.resources_dir, f"{ticker.lower()}-{fiscal_year}.html")

    def _load_html(self, file_path):
        """
        Loads the HTML content of a file using LangChain's UnstructuredHTMLLoader.
        """
        return UnstructuredHTMLLoader(file_path).load()

    def _extract_sections(self, html_content, section_titles):
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

    def _clean_sections(self, sections):
        """
        Cleans sections by removing overlapping text from subsequent section titles.
        """
        cleaned_sections = {}
        for section_title, content in sections.items():
            current_index = next((i for i, item in enumerate(self.index_info) if item.lower().startswith(section_title.lower())), None)
            if current_index is not None:
                next_section = self.index_info[current_index + 1] if current_index + 1 < len(self.index_info) else None
                if next_section:
                    next_section_pattern = re.escape(next_section) + r"(\s*continued)*"
                    next_section_match = re.search(next_section_pattern, content, re.IGNORECASE)
                    if next_section_match:
                        content = content[:next_section_match.start()].strip()
                if content:
                    cleaned_sections[section_title] = content
        return cleaned_sections

    def _split_and_store_chunks(self, section_name, content, output_dir):
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

    def process_file(self, files_metadata):
        """
        Processes a single file based on metadata, extracting and chunking sections.
        """
        if not files_metadata or len(files_metadata) != 1:
            raise ValueError("files_metadata should contain exactly one item.")

        metadata = files_metadata[0]
        ticker, fiscal_year = metadata["ticker"], metadata["fiscal_year"]
        output_dir = f"main_{ticker}-{fiscal_year}" if ticker == "tsla" and fiscal_year == 20231231 else f"sub_{ticker}-{fiscal_year}"
        self.file_dir = output_dir

        file_path = self._construct_file_path(ticker, fiscal_year)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File for {ticker} FY{fiscal_year} not found.")

        documents = self._load_html(file_path)
        document_text = documents[0].page_content

        section_titles = [self.items[key][0] for key in self.items]
        extracted_sections = self._extract_sections(document_text, section_titles)
        cleaned_sections = self._clean_sections(extracted_sections)

        os.makedirs(output_dir, exist_ok=True)
        results = {section: self._split_and_store_chunks(section, content, output_dir) for section, content in cleaned_sections.items() if content}
        self.metadata[f"{ticker.upper()}_FY{fiscal_year}"] = {"file_path": file_path, "sections_processed": list(results.keys())}
        return results

    def classify_files(self, files_metadata=None):
        """
        Classifies JSON files into directories based on section categories.
        """
        if not hasattr(self, 'file_dir'):
            raise ValueError("File directory not set. Ensure process_file is run first.")

        categories = [item[0] for item in self.items.values()]
        summary = {"metadata": files_metadata if files_metadata else []}

        for category in categories:
            category_dir = os.path.join(self.file_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            summary[category] = {"chunk_count": 0}

        for filename in os.listdir(self.file_dir):
            if filename.endswith(".json"):
                for category in categories:
                    if filename.lower().startswith(category.lower()):
                        src_path = os.path.join(self.file_dir, filename)
                        dest_path = os.path.join(self.file_dir, category, filename)
                        shutil.move(src_path, dest_path)
