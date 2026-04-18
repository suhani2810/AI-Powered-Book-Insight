import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="books")

model = SentenceTransformer("all-MiniLM-L6-v2")


def chunk_text(text, size=300, overlap=50):
    chunks = []
    i = 0

    while i < len(text):
        chunks.append(text[i:i+size])
        i += size - overlap

    return chunks


def load_books_into_db(books):
    for book in books:
        collection.delete(where={"title": book.title})

        text = (book.description or "") + " " + (book.summary or "")
        chunks = chunk_text(text)

        for idx, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"title": book.title}],
                ids=[f"{book.id}_{idx}"]
            )


def query_books(question):
    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results