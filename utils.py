import os
import openai
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain import HuggingFaceHub
from langchain.schema import Document
from langchain.vectorstores import Pinecone
import pinecone
from pypdf import PdfReader

def get_pdf_text(pdf_doc):
    pdf_reader = PdfReader(pdf_doc)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    print('get pdf text')

    return text


def create_docs(user_pdf_list, unique_id):
    docs = []
    for filename in user_pdf_list:
        chunks = get_pdf_text(filename)

        metadata = {
            "name": filename.name,
            "type": filename.type,
            "size": filename.size,
            "unique_id": unique_id
        }

        docs.append(Document(page_content=chunks, metadata=metadata))

    print('create docs')

    return docs


def create_embeddings():
    embeddings = OpenAIEmbeddings()

    return embeddings


def push_to_pinecone(environment, index_name, embeddings, docs):
    pinecone.init(
        api_key=os.environ['PINECONE_API_KEY'],
        environment=environment
    )
    Pinecone.from_documents(docs,embeddings, index_name=index_name)
    print('push to pinecone')


def pull_from_pinecone(environment, index_name, embeddings):
    pinecone.init(
        api_key=os.environ['PINECONE_API_KEY'],
        environment=environment
    )
    
    index = Pinecone.from_existing_index(index_name, embeddings)
    print('pull from pinecone')

    return index


def similar_docs(query, resume_count, environment, index_name, embeddings, unique_id):
    pinecone.init(
        api_key=os.environ['PINECONE_API_KEY'],
        environment=environment
    )

    index = pull_from_pinecone(environment, index_name, embeddings)
    # similar_docs = index.similarity_search_with_score(query, int(resume_count), {"unique_id": unique_id})
    similar_docs = index.similarity_search(query, k=int(resume_count))
    # print(similar_docs)
    print('similar docs')

    return similar_docs


def get_summary(doc):
    llm = OpenAI()
