from app.services.milvus_service import MilvusService


# Milvus service

milvus_service = MilvusService()


# SQL subject id from MongoDB

subject_id = "6ab7ecb607ce2173b3d2b738"


# Delete SQL records from Milvus

delete_result = milvus_service.delete_by_subject(
    subject_id
)


print("\nDeletion completed")
print(delete_result)