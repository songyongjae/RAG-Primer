from utils import TextProcessor
import os
import json
from tqdm import tqdm
from typing import List, Dict
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
import shutil
from sentence_transformers import util

class ChunkProcessor:
    def __init__(self, resources_dir, model_name, pca_components, dbscan_eps, dbscan_min_samples):
        self.resources_dir = resources_dir
        self.text_processor = TextProcessor(model_name, pca_components, dbscan_eps, dbscan_min_samples)

    def process_section(self, ticker: str, fiscal_year: int, section_name: str, content: str, output_dir: str) -> Dict:
        splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=150)
        chunks = splitter.split_text(content)
        chunk_files = []
        for i, chunk in enumerate(chunks):
            output_file_path = os.path.join(output_dir, f"{section_name}_chunk_{i + 1}.json")
            with open(output_file_path, 'w', encoding='utf-8') as json_file:
                json.dump({"chunk": chunk, "chunk_index": i + 1}, json_file, indent=4)
            chunk_files.append(output_file_path)
        logging.info(f"Processed {len(chunks)} chunks for section '{section_name}'.")
        return {"section": section_name, "chunk_count": len(chunks), "chunk_files": chunk_files}

    def categorize_chunks(self, output_dir: str, chunk_files: List[str]):
        keywords = {
            "ITEM 1.": "Description of Business",
            "ITEM 1A.": "Risk Factors",
            "ITEM 7.": "Management's Discussion and Analysis of Financial Condition and Results of Operations"
        }
        keyword_embeddings = {key: self.text_processor.model.encode(value, convert_to_tensor=True) for key, value in keywords.items()}
        for key in keywords.keys():
            os.makedirs(os.path.join(output_dir, key), exist_ok=True)
        folder_file_counts = {key: 0 for key in keywords.keys()}

        for chunk_file in tqdm(chunk_files, desc="Categorizing chunks", leave=False):
            with open(chunk_file, 'r', encoding='utf-8') as file:
                chunk_data = json.load(file)
                chunk_text = chunk_data["chunk"]
            chunk_embedding = self.text_processor.model.encode(chunk_text, convert_to_tensor=True)
            similarities = {key: util.pytorch_cos_sim(chunk_embedding, embed).item() for key, embed in keyword_embeddings.items()}
            best_fit = max(similarities, key=similarities.get)
            folder_file_counts[best_fit] += 1
            new_file_name = f"{best_fit}_chunk_{folder_file_counts[best_fit]}.json"
            shutil.move(chunk_file, os.path.join(output_dir, best_fit, new_file_name))
        logging.info("Chunks categorized into respective sections.")
