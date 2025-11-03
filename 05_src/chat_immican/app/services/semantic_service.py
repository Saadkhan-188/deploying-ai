# Chroma client, embedding wrappers, hybrid psql metadata sync# app/services/semantic_service.py
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings as ChromaSettings
import pandas as pd
from typing import List, Dict

from app.config import settings

class SemanticService:
    def __init__(self, persist_dir=None, model_name=None, collection_name="faqs"):
        self.persist_dir = persist_dir or settings.CHROMA_PERSIST_DIR
        os.makedirs(self.persist_dir, exist_ok=True)
        self.client = chromadb.Client(ChromaSettings(persist_directory=self.persist_dir))
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = SentenceTransformer(self.model_name)
        self.collection_name = collection_name
        # try load or create
        try:
            self.collection = self.client.get_collection(self.collection_name)
        except Exception:
            self.collection = self.client.create_collection(self.collection_name)
            # ingest sample CSV if present
            csv_path = "faqs.csv"
            if os.path.exists(csv_path):
                self._ingest_csv(csv_path)

    def _ingest_csv(self, csv_path):
        df = pd.read_csv(csv_path)
        texts = (df['title'] + "\n" + df['content']).tolist()
        ids = df['id'].astype(str).tolist()
        metas = df[['title','content']].to_dict(orient='records')
        embeddings = self.model.encode(texts).tolist()
        self.collection.add(ids=ids, embeddings=embeddings, metadatas=metas, documents=texts)
        self.client.persist()

    def query(self, query_text: str, k=3):
        emb = self.model.encode([query_text])[0].tolist()
        out = self.collection.query(query_embeddings=[emb], n_results=k)
        results=[]
        for i in range(len(out['ids'][0])):
            results.append({
                "id": out['ids'][0][i],
                "document": out['documents'][0][i],
                "metadata": out['metadatas'][0][i],
                "distance": out['distances'][0][i]
            })
        return results

    def answer(self, question: str):
        hits = self.query(question, k=2)
        if not hits:
            return "I couldn't find relevant info in the knowledge base."
        top = hits[0]['metadata']['content']
        # deterministic rephrase: extract lead sentence and return directive
        lead = top.split(".")[0]
        answer = f"{lead}. I can expand with steps if you'd like."
        if len(hits)>1:
            answer += f" Also see: {hits[1]['metadata']['title']}."
        return answer
