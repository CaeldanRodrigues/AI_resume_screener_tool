import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain import HuggingFaceHub
from langchain.schema import Document
import pinecone
from pypdf import PdfReader

def get_pdf_text(pdf_doc):
    pdf_reader = PdfReader(pdf_doc)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    return text


def create_docs(user_pdf_list, unique_id):
    docs = []
    for filename in user_pdf_list:
        chunks = get_pdf_text(filename)

        metadata = {
            "name": filename.name,
            "id": filename.id,
            "type": filename.type,
            "size": filename.size,
            "unique_id": unique_id
        }

        docs.append(Document(page_content=chunks, metadata=metadata))

    return docs

