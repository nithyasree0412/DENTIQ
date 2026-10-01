from pathlib import Path

import numpy as np

from pymilvus import MilvusClient


class MilvusService:

    def __init__(self):

        project_root = Path(__file__).resolve().parents[2]

        self.milvus_db = str(
            project_root / "bds_rag.db"
        )

        self.collection_name = "subject_documents"

        self.client = MilvusClient(
            uri=self.milvus_db
        )

        print("Milvus connected")

    def create_collection(
        self,
        collection_name="subject_documents",
        dimension=384
    ):

        self.collection_name = collection_name

        if self.client.has_collection(
            collection_name
        ):

            self.client.drop_collection(
                collection_name
            )

        self.client.create_collection(
            collection_name=collection_name,
            dimension=dimension,
            metric_type="COSINE"
        )

    def load_collection(self):

        self.client.load_collection(
            collection_name=self.collection_name
        )

    def prepare_data(
        self,
        chunks,
        chunk_embeddings,
        subject_id,
        subject_name
    ):

        data = []

        for i, chunk in enumerate(chunks):

            data.append({
                "id": i,
                "vector": chunk_embeddings[i].tolist(),
                "text": chunk["text"],
                "subject_id": subject_id,
                "subject": subject_name,
                "page": chunk["page"]
            })

        return data

    def insert_data(
        self,
        data
    ):

        insert_result = self.client.insert(
            collection_name=self.collection_name,
            data=data
        )

        return insert_result

    def search(
        self,
        query_embedding,
        subject_id,
        limit=5
    ):

        self.load_collection()

        search_results = self.client.search(
            collection_name=self.collection_name,
            data=[query_embedding],
            filter=f'subject_id == "{subject_id}"',
            limit=limit,
            output_fields=[
                "text",
                "subject_id",
                "subject",
                "page"
            ]
        )

        return search_results

    def get_random_candidates(
        self,
        subject_id,
        num_candidates=40
    ):

        self.load_collection()

        records = self.client.query(
            collection_name=self.collection_name,
            filter=f'subject_id == "{subject_id}"',
            output_fields=[
                "id",
                "vector",
                "text",
                "subject_id",
                "subject",
                "page"
            ]
        )

        if not records:
            return []

        num_candidates = min(
            num_candidates,
            len(records)
        )

        selected_indices = np.random.choice(
            len(records),
            size=num_candidates,
            replace=False
        )

        candidates = [
            records[index]
            for index in selected_indices
        ]

        return candidates

    def delete_by_subject(
        self,
        subject_id
    ):

        delete_result = self.client.delete(
            collection_name=self.collection_name,
            filter=f'subject_id == "{subject_id}"'
        )

        return delete_result