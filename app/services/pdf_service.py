import fitz

from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFService:

    def extract_text_from_pdf(self, pdf_path):

        document = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(document):

            text = page.get_text()

            if text.strip():
                pages.append({
                    "page": page_number + 1,
                    "text": text
                })

        document.close()

        return pages

    def split_text(
        self,
        pages,
        chunk_size=500,
        chunk_overlap=50
    ):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

        chunks = []

        for page in pages:

            page_chunks = text_splitter.split_text(
                page["text"]
            )

            for chunk in page_chunks:

                chunks.append({
                    "text": chunk,
                    "page": page["page"]
                })

        return chunks