import os
import sys
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

for key in ("OPENAI_API_KEY","PGVECTOR_URL","PGVECTOR_COLLECTION","PDF_PATH"):
    if not os.getenv(key):
        raise RuntimeError(f"Environment variable {key} is not set.")
    
PDF_PATH = os.getenv("PDF_PATH")

def resolve_pdf_path():
    repo_root = Path(__file__).resolve().parents[1]

    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        return p.resolve() if p.is_absolute() else (repo_root / p).resolve()

    pdf_env = os.getenv("PDF_PATH", "document.pdf")
    p = Path(pdf_env)
    return p.resolve() if p.is_absolute() else (repo_root / p).resolve()

def ingest_pdf():
    
    pdf_path = resolve_pdf_path()
    
    if not pdf_path.exists():
        print(f"PDF file not found: {pdf_path}")
        return
    
    docs = PyPDFLoader(str(pdf_path)).load()

    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False).split_documents(docs)
    
    if not splits:
        print(f"No document splits were created from the PDF.")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )
    
    store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True,
    )

    ids = [f"{pdf_path.stem}-chunk-{i}" for i in range(len(splits))]

    store.add_documents(documents=splits, ids=ids)
    print(f"Ingestion completed successfully. {len(splits)} document splits were added to the vector store.")

if __name__ == "__main__":
    ingest_pdf()