import os
import uuid
from pathlib import Path

# Streamlit Community Cloud currently runs a protobuf/chromadb combination
# that is more reliable with the pure-Python protobuf implementation.
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

import chromadb
import pandas as pd

class Portfolio:
    def __init__(self, file_path=None):
        base_dir = Path(__file__).resolve().parent
        self.file_path = Path(file_path) if file_path else base_dir / "Portfolio.csv"
        self.data = pd.read_csv(self.file_path)
        self.chroma_client = chromadb.PersistentClient(path=str(base_dir / "vectorstore"))
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Programming"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())],
                )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get("metadatas", [])
