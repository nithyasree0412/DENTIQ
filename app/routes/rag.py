from fastapi import APIRouter

from services.pdf_service import PDFService
from services.embedding_service import EmbeddingService
from services.milvus_service import MilvusService
from services.llm_service import LLMService
from services.rag_service import RAGService

router = APIRouter()

pdf_service = PDFService()
embedding_service = EmbeddingService()
milvus_service = MilvusService()
llm_service = LLMService()

rag_service = RAGService(
    embedding_service=embedding_service,
    milvus_service=milvus_service,
    llm_service=llm_service
)


@router.post("/doubt")
def answer_doubt(data: dict):

    user_query = data["question"]
    subject_id = data["subjectId"]

    answer = rag_service.answer_doubt(
        user_query=user_query,
        subject_id=subject_id
    )

    return {
        "answer": answer
    }


@router.post("/test")
def generate_test(data: dict):

    subject_id = data["subjectId"]
    num_questions = data["numQuestions"]

    result = rag_service.generate_test(
        subject_id=subject_id,
        num_questions=num_questions
    )

    return {
        "result": result
    }


@router.post("/ingest")
def ingest_pdf(data: dict):

    pdf_path = data["pdfPath"]
    subject_id = data["subjectId"]
    subject_name = data["subjectName"]

    pages = pdf_service.extract_text_from_pdf(
        pdf_path
    )

    chunks = pdf_service.split_text(
        pages
    )

    chunk_embeddings = embedding_service.embed_documents(
        chunks
    )

    milvus_data = milvus_service.prepare_data(
        chunks,
        chunk_embeddings,
        subject_id,
        subject_name
    )

    insert_result = milvus_service.insert_data(
        milvus_data
    )

    return {
        "message": "PDF processed and added to Milvus successfully",
        "subjectId": subject_id,
        "subjectName": subject_name,
        "pages": len(pages),
        "chunks": len(chunks),
        "insert_count": insert_result["insert_count"]
    }