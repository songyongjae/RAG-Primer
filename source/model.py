import os
import shutil
import json
from utils import (
    _construct_file_path, _load_html, _extract_sections, _clean_sections, _split_and_store_chunks
)
from config import ITEMS, INDEX_INFO, RESOURCES_DIR

class get_sources_10k:
    def __init__(self, resources_dir=RESOURCES_DIR):
        self.resources_dir = resources_dir
        self.metadata = {}
        self.items = ITEMS
        self.index_info = INDEX_INFO

    def process_file(self, files_metadata):
        if not files_metadata or len(files_metadata) != 1:
            raise ValueError("files_metadata should contain exactly one item.")
        metadata = files_metadata[0]
        ticker, fiscal_year = metadata["ticker"], metadata["fiscal_year"]
        output_dir = f"main_{ticker}-{fiscal_year}" if ticker == "tsla" and fiscal_year == 20231231 else f"sub_{ticker}-{fiscal_year}"
        self.file_dir = output_dir

        file_path = _construct_file_path(self.resources_dir, ticker, fiscal_year)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File for {ticker} FY{fiscal_year} not found.")

        documents = _load_html(file_path)
        document_text = documents[0].page_content
        section_titles = [self.items[key][0] for key in self.items]
        extracted_sections = _extract_sections(document_text, section_titles, self.index_info)
        cleaned_sections = _clean_sections(extracted_sections, self.index_info)

        os.makedirs(output_dir, exist_ok=True)
        results = {section: _split_and_store_chunks(section, content, output_dir) for section, content in cleaned_sections.items() if content}
        self.metadata[f"{ticker.upper()}_FY{fiscal_year}"] = {"file_path": file_path, "sections_processed": list(results.keys())}
        return results

    def classify_files(self, files_metadata=None):
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
                        summary[category]["chunk_count"] += 1
                        break
        return json.dumps(summary, indent=4)
