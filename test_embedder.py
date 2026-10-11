from src.embedder import embed_texts, embed_query

texts = [
    "I love dogs and puppies",
    "The stock market fell today",
    "Puppies are wonderful pets",
]

vectors = embed_texts(texts)
print(f"Generated {len(vectors)} vectors")
print(f"Each vector has {len(vectors[0])} dimensions\n")

# Compare similarity
q = embed_query("Do you like dogs?")
print(f"Query embedded into {len(q)} dimensions")

# Compute cosine similarity manually
import math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb)

for i, v in enumerate(vectors):
    score = cosine(q, v)
    print(f"Similarity to '{texts[i]}': {score:.3f}")