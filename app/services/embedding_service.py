from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(
        self,
        model_name="BAAI/bge-small-en-v1.5"
    ):
        self.model_name = model_name

        self.model = SentenceTransformer(
            self.model_name,
            device="cuda"
        )

    def embed_documents(
        self,
        chunks,
        batch_size=32
    ):

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        return embeddings

    def embed_query(
        self,
        user_query
    ):

        query_embedding = self.model.encode(
            user_query,
            normalize_embeddings=True
        )

        return query_embedding.tolist()