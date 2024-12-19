from bs4 import BeautifulSoup
import logging
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sentence_transformers import SentenceTransformer

def extract_sections(document_text, model, pca_components=25, dbscan_eps=0.5, dbscan_min_samples=2):
    """
    Extracts sections from the document using clustering on text embeddings.

    :param document_text: Full text of the document.
    :param model: Pre-trained SentenceTransformer model.
    :param pca_components: Number of PCA components for dimensionality reduction.
    :param dbscan_eps: DBSCAN epsilon parameter for clustering.
    :param dbscan_min_samples: Minimum samples for DBSCAN clustering.
    :return: Dictionary of extracted sections.
    """
    soup = BeautifulSoup(document_text, "html.parser")
    text_blocks = [tag.get_text(strip=True) for tag in soup.find_all(["p", "li", "div"]) if tag.get_text(strip=True)]

    if not text_blocks:
        logging.warning("No text blocks found, returning entire document as 'general'.")
        return {"general": document_text.strip()}

    embeddings = model.encode(text_blocks, convert_to_tensor=True)
    pca = PCA(n_components=pca_components)
    reduced_embeddings = pca.fit_transform(embeddings.cpu().detach().numpy())
    clustering = DBSCAN(eps=dbscan_eps, min_samples=dbscan_min_samples).fit(reduced_embeddings)
    labels = clustering.labels_

    if all(label == -1 for label in labels):
        logging.warning("All blocks classified as noise by DBSCAN. Returning entire text as 'general'.")
        return {"general": "\n".join(text_blocks)}

    clusters = {}
    for idx, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(text_blocks[idx])

    return {f"Cluster-{i}": "\n".join(content) for i, content in clusters.items()}
