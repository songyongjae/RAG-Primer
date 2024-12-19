def combine_content(documents):
    """
    Combines the 'chunk' content from all documents into a single string.

    :param documents: List of documents loaded from JSON files.
    :return: Combined content as a single string.
    """
    return "\n\n".join(doc.get('chunk', '') for doc in documents)
