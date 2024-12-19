import os
import json
import shutil
from sentence_transformers import util

def categorize_chunks(chunk_files, output_dir, model, keywords):
    """
    Categorizes chunks into predefined sections using similarity scores.

    :param chunk_files: List of chunk file paths.
    :param output_dir: Directory to save categorized chunks.
    :param model: Pre-trained SentenceTransformer model.
    :param keywords: Dictionary of keywords for predefined sections.
    """
    keyword_embeddings = {key: model.encode(value, convert_to_tensor=True) for key, value in keywords.items()}

    for key in keywords.keys():
        os.makedirs(os.path.join(output_dir, key), exist_ok=True)
    folder_file_counts = {key: 0 for key in keywords.keys()}

    for chunk_file in chunk_files:
        with open(chunk_file, 'r', encoding='utf-8') as file:
            chunk_data = json.load(file)
            chunk_text = chunk_data["chunk"]
        chunk_embedding = model.encode(chunk_text, convert_to_tensor=True)
        similarities = {key: util.pytorch_cos_sim(chunk_embedding, embed).item() for key, embed in keyword_embeddings.items()}
        best_fit = max(similarities, key=similarities.get)
        folder_file_counts[best_fit] += 1
        new_file_name = f"{best_fit}_chunk_{folder_file_counts[best_fit]}.json"
        shutil.move(chunk_file, os.path.join(output_dir, best_fit, new_file_name))
