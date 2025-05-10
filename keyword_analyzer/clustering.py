import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from config import EMBEDDING_MODEL, CLUSTERING_DISTANCE_THRESHOLD

def cluster_keywords(input_csv, clusters_output):
    """Process keywords and create clusters"""
    df = pd.read_csv(input_csv)
    if 'keyword' not in df.columns:
        raise ValueError("Input CSV must contain 'keyword' column")
    
    # Preprocess keywords
    keywords = df['keyword'].astype(str).str.lower().dropna().unique()
    keywords = sorted(keywords)

    # Generate embeddings
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode(keywords, convert_to_numpy=True)

    # Cluster embeddings
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=CLUSTERING_DISTANCE_THRESHOLD,
        metric='cosine',
        linkage='average'
    )
    labels = clustering.fit_predict(embeddings)

    # Save clusters
    cluster_df = pd.DataFrame({'keyword': keywords, 'cluster_id': labels})
    cluster_summary = cluster_df.groupby('cluster_id')['keyword'].agg('; '.join).reset_index()
    cluster_summary.to_csv(clusters_output, index=False)
    
    return cluster_summary