import os
import json

def read_documents(folder_paths, filter_items):
    """
    Reads JSON files from the specified folder paths and filters them by the filter_items.

    :param folder_paths: List of folder paths to search for JSON files.
    :param filter_items: List of filter keywords to match file names.
    :return: List of document contents as dictionaries.
    """
    documents = []
    for folder_path in folder_paths:
        _process_folder(folder_path, filter_items, documents)
    return documents

def _process_folder(folder_path, filter_items, documents):
    """
    Processes each folder, finds matching JSON files, and loads their content.

    :param folder_path: Path to the folder to process.
    :param filter_items: List of filter keywords.
    :param documents: List to store loaded JSON contents.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Folder path {folder_path} does not exist.")
        return

    for file in os.listdir(folder_path):
        if file.endswith('.json') and any(item.lower() in file.lower() for item in filter_items):
            _load_file(os.path.join(folder_path, file), documents)

def _load_file(file_path, documents):
    """
    Loads a JSON file and appends its content to the documents list.

    :param file_path: Path to the JSON file.
    :param documents: List to store loaded JSON contents.
    """
    try:
        with open(file_path, 'r') as f:
            content = json.load(f)
            if 'chunk' not in content:
                print(f"Warning: 'chunk' key missing in {os.path.basename(file_path)}")
            documents.append(content)
    except Exception as e:
        print(f"Error loading file {os.path.basename(file_path)}: {e}")
