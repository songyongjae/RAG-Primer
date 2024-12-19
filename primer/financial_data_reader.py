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
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            for file in files:
                if file.endswith('.json') and any(item.lower() in file.lower() for item in filter_items):
                    file_path = os.path.join(folder_path, file)
                    try:
                        with open(file_path, 'r') as f:
                            content = json.load(f)
                            if 'chunk' not in content:
                                print(f"Warning: 'chunk' key missing in {file}")
                            documents.append(content)
                    except Exception as e:
                        print(f"Error loading file {file}: {e}")
        else:
            print(f"Error: Folder path {folder_path} does not exist.")
    return documents
