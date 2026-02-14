import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import logging
from typing import List, Dict, Any, Optional
import uuid

load_dotenv()
logger = logging.getLogger(__name__)

class MemoryModule:
    def __init__(self, collection_name: str = "spatial_memory"):
        self.collection_name = collection_name
        self.url = os.getenv("QDRANT_URL")
        self.api_key = os.getenv("QDRANT_API_KEY")
        
        if self.url:
            self.client = QdrantClient(url=self.url, api_key=self.api_key)
        else:
            self.client = QdrantClient(":memory:")
            
        self._ensure_collection()
        # We need an embedding function. For simplicity, we'll use a mock or reuse Gemini if text.
        # But for spatial memory (x,y), we might use coordinate vectors directly?
        # Actually, the plan says "Storing environment maps and object interactions"
        # We'll store textual descriptions of locations: "Obstacle at (3,4)" 
        # and embed them using Gemini.

    def _ensure_collection(self):
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )

    def store_memory(self, text: str, metadata: Dict[str, Any], embedding: List[float]):
        point_id = str(uuid.uuid4())
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={"text": text, **metadata}
                )
            ]
        )
        return point_id

    def search_memory(self, query_embedding: List[float], limit: int = 5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )
        return [{"text": r.payload.get("text"), "score": r.score, "metadata": r.payload} for r in results]
