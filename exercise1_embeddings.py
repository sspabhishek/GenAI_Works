#!/usr/bin/env python3
"""
Exercise 1: Text Embeddings & Similarity Comparison
Generates embeddings using Sentence Transformers and computes cosine similarity.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample sentences
sentences = [
    "GenAI is transforming software development",
    "Artificial Intelligence is changing how developers work",
    "I love playing cricket on weekends",
    "Machine learning models power modern AI applications",
    "Software engineers build the future with code"
]

print("=" * 70)
print("Exercise 1: Text Embeddings & Similarity Comparison")
print("=" * 70)

# Load the Sentence Transformer model
print("\n[1] Loading model: all-MiniLM-L6-v2...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✓ Model loaded successfully")

# Generate embeddings
print("\n[2] Generating embeddings for sentences...")
embeddings = model.encode(sentences)
print(f"✓ Generated {len(embeddings)} embeddings of dimension {embeddings[0].shape[0]}")

# Display first 5 dimensions of each embedding
print("\n[3] First 5 dimensions of each embedding:")
print("-" * 70)
for i, (sentence, embedding) in enumerate(zip(sentences, embeddings)):
    first_5_dims = embedding[:5]
    print(f"\nSentence {i+1}: {sentence}")
    print(f"First 5 dimensions: {first_5_dims}")

# Compute cosine similarity matrix
print("\n[4] Computing cosine similarity between all pairs...")
similarity_matrix = cosine_similarity(embeddings)

# Display similarity matrix
print("\n[5] Similarity Score Matrix:")
print("-" * 70)

# Header row with sentence indices
print("\nSentence indices (rows vs columns):")
for i in range(len(sentences)):
    print(f"  {i+1}: {sentences[i][:50]}...")

print("\n\nSimilarity Matrix:")
print("     ", end="")
for j in range(len(sentences)):
    print(f"   S{j+1}  ", end="")
print()

for i in range(len(sentences)):
    print(f"S{i+1}: ", end="")
    for j in range(len(sentences)):
        print(f" {similarity_matrix[i][j]:6.4f}", end="")
    print()

# Find and display highest and lowest similarity pairs
print("\n[6] Similarity Insights:")
print("-" * 70)

# Get upper triangle to avoid duplicates
similarity_pairs = []
for i in range(len(sentences)):
    for j in range(i+1, len(sentences)):
        similarity_pairs.append((similarity_matrix[i][j], i, j))

similarity_pairs.sort(reverse=True)

print("\nHighest Similarity Pairs:")
for sim, i, j in similarity_pairs[:3]:
    print(f"  S{i+1} <-> S{j+1}: {sim:.4f}")
    print(f"    '{sentences[i]}'")
    print(f"    '{sentences[j]}'")

print("\nLowest Similarity Pairs:")
for sim, i, j in similarity_pairs[-3:]:
    print(f"  S{i+1} <-> S{j+1}: {sim:.4f}")
    print(f"    '{sentences[i]}'")
    print(f"    '{sentences[j]}'")

