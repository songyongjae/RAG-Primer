from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer, util
import logging
import os
import json
from bs4 import BeautifulSoup
from typing import Dict

class TextProcessor:
    def __init__(self, model_name, pca_components, dbscan_eps, dbscan_min_samples):
        self.model = SentenceTransformer(model_name)
        self.pca_components = pca_components
        self.dbscan_eps = dbscan_eps
        self.dbscan_min_samples = dbscan_min_samples

    def extract_sections(self, document_text: str) -> Dict[str, str]:
        soup = BeautifulSoup(document_text, "html.parser")
        text_blocks = [tag.get_text(strip=True) for tag in soup.find_all(["p", "li", "div"]) if tag.get_text(strip=True)]

        if not text_blocks:
            logging.warning("No text blocks found, returning entire document as 'general'.")
            return {"general": document_text.strip()}

        embeddings = self.model.encode(text_blocks, convert_to_tensor=True)
        pca = PCA(n_components=self.pca_components)
        reduced_embeddings = pca.fit_transform(embeddings.cpu().detach().numpy())
        clustering = DBSCAN(eps=self.dbscan_eps, min_samples=self.dbscan_min_samples).fit(reduced_embeddings)
        labels = clustering.labels_

        if all(label == -1 for label in labels):
            logging.warning("All blocks classified as noise by DBSCAN. Returning entire text as 'general'.")
            return {"general": "\n".join(text_blocks)}

        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(text_blocks[idx])

        sections = {f"Cluster-{i}": "\n".join(content) for i, content in clusters.items()}
        sections["general"] = "\n".join(clusters.get(max(clusters, key=lambda x: len(clusters[x])), []))
        return sections
