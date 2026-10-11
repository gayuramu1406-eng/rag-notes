from src.indexer import index_documents

docs = [
    {"source": "fake_note.txt", "text": "My favorite color is teal. I like it because it feels calm."},
    {"source": "fake_note2.txt", "text": "Python was created by Guido van Rossum in 1991."},
]

stats = index_documents(docs)
print(stats)