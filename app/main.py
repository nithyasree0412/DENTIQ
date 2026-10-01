from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routes.rag import router as rag_router
from middleware.error import error_handler

app = FastAPI()

app.add_exception_handler(
    Exception,
    error_handler
)

app.include_router(
    rag_router,
    prefix="/api/v1/rag"
)


@app.get("/")
def root():
    return {
        "message": "DENTIQ AI Service is running"
    }