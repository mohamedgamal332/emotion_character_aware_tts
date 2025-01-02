import numpy as np
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
from rapidfuzz.distance import Levenshtein
from sklearn.cluster import DBSCAN

# Input: List of sentences
sentences = json.load(open("../temp/flat-text.json", "r", encoding="utf-8"))

# Extract names
names = json.load(open("../temp/characters.json", "r", encoding="utf-8"))

# Step 2: Embed sentences
model = SentenceTransformer('all-MiniLM-L6-v2')  # Compact and fast model
sentence_embeddings = model.encode(sentences)

# Step 3: Compute semantic similarity between names using sentence context
def compute_semantic_similarity(names, sentences, embeddings):
    name_to_sentence = {name: [sent for sent in sentences if name in sent.lower()] for name in names}
    name_embeddings = {
        name: np.mean([embeddings[sentences.index(sent)] for sent in associated_sentences], axis=0)
        if associated_sentences else np.zeros(embeddings.shape[1])
        for name, associated_sentences in name_to_sentence.items()
    }
    return cosine_similarity(list(name_embeddings.values()))

semantic_similarity_matrix = compute_semantic_similarity(names, sentences, sentence_embeddings)

# Step 4: Compute string similarity matrix
def compute_string_similarity_matrix(names):
    n = len(names)
    similarity_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            similarity_matrix[i, j] = 1 - (Levenshtein.distance(names[i], names[j]) / max(len(names[i]), len(names[j])))
    return similarity_matrix

string_similarity_matrix = compute_string_similarity_matrix(names)

# Step 5: Combine semantic and string similarity
combined_similarity_matrix = 0.7 * semantic_similarity_matrix + 0.3 * string_similarity_matrix

# Step 6: Clustering
clustering = AgglomerativeClustering(
    n_clusters= None, #None, #Let it decide the number of clusters
    distance_threshold=0,  # Adjust for tighter/looser clusters
    affinity='precomputed',
    linkage='average'
)
labels = clustering.fit_predict(1 - combined_similarity_matrix)  # Convert similarity to distance

# Step 7: Group names by clusters
clusters = {}
for name, label in zip(names, labels):
    clusters.setdefault(label, []).append(name)

# Output the clusters
for cluster_id, cluster_names in clusters.items():
    print(f"Cluster {cluster_id}: {cluster_names}")

char_dict = {"Narrator": "Narrator"}
for ndx, chars in clusters.items():
    for i in chars:
        char_dict[i] = chars[0]

json.dump(char_dict, open("../temp/char_dict.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)