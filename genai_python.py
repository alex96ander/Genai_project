import os
import hashlib
from typing import List, Dict, Any
from google import genai  # Standard Google GenAI SDK
from redis import Redis
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.index_definition import (
    IndexDefinition,
    IndexType
)

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False

class ProfanityFilter:
    """Uses a Trie data structure to find banned words in O(N) time."""
    def __init__(self, banned_words: List[str]):
        self.root = TrieNode()
        for word in banned_words:
            self.insert(word.lower())

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def contains_profanity(self, text: str) -> bool:
        text = text.lower()
        words = text.split()
        for word in words:
            node = self.root
            for char in word:
                if char not in node.children:
                    break
                node = node.children[char]
                if node.is_end_of_word:
                    return True
        return False

class AIService:
    def __init__(self):
        # Initializes the standard Gemini client
        self.client = genai.Client()
        self.model_id = "gemini-2.5-flash"

    def get_embedding(self, text: str) -> List[float]:
        """Generates vector embeddings for semantic search."""
        response = self.client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return response.embeddings[0].values

    def analyze_toxicity(self, text: str) -> str:
        """Uses LLM to analyze subtle context/toxicity."""
        prompt = f"Analyze the following text for hidden toxicity, hate speech, or harassment. Respond with only 'SAFE' or 'TOXIC':\n\n\"{text}\""
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text.strip()


class ContentPipeline:
    def __init__(self, banned_words: List[str]):
        # Connect to local Redis instance
        self.redis = Redis(host='localhost', port=6379, decode_responses=False)
        self.dsa_filter = ProfanityFilter(banned_words)
        self.ai = AIService()
        self._setup_redis_vector_index()

    def _setup_redis_vector_index(self):
        """Creates a schema in Redis for Vector Similarity Search (VSS)."""
        try:
            schema = (
                TextField("text"),
                VectorField("embedding", "HNSW", {
                    "TYPE": "FLOAT32", 
                    "DIM": 768, 
                    "DISTANCE_METRIC": "COSINE"
                })
            )
            self.redis.ft("idx:content").create_index(
                schema, 
                definition=IndexDefinition(prefix=["content:"], index_type=IndexType.HASH)
            )
        except Exception:
            pass  # Index already exists

    def process_text(self, text: str) -> Dict[str, Any]:
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        cache_key = f"cache:status:{text_hash}"
        cached_status = self.redis.get(cache_key)
        
        if cached_status:
            return {"text": text, "status": cached_status.decode('utf-8'), "source": "cache"}

        if self.dsa_filter.contains_profanity(text):
            self.redis.setex(cache_key, 3600, "BLOCKED_BY_TRIE")
            return {"text": text, "status": "BLOCKED_BY_TRIE", "source": "trie"}

        ai_status = self.ai.analyze_toxicity(text)
        
        if ai_status == "TOXIC":
            self.redis.setex(cache_key, 3600, "BLOCKED_BY_AI")
            return {"text": text, "status": "BLOCKED_BY_AI", "source": "ai"}

        embedding = self.ai.get_embedding(text)
        import numpy as np
        embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()

        pipeline = self.redis.pipeline()
        pipeline.hset(f"content:{text_hash}", mapping={
            "text": text,
            "embedding": embedding_bytes
        })
        pipeline.setex(cache_key, 3600, "APPROVED")
        pipeline.execute()

        return {"text": text, "status": "APPROVED", "source": "ai_processed"}


if __name__ == "__main__":
    banned = ["badword", "scam", "malware"]
    pipeline = ContentPipeline(banned_words=banned)
    print(pipeline.process_text("Click here for a scam link")) 
    print(pipeline.process_text("I absolutely despise everything you stand for and hope you fail.")) 
    print(pipeline.process_text("Python algorithms mixed with Redis make platforms scale wonderfully."))
