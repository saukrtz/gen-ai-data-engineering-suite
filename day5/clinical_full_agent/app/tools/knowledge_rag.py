import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def setup_rag():
    data_path = os.path.join(os.path.dirname(__file__), "../../data/clinical_guidelines.txt")
    
    if not os.path.exists(data_path):
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        with open(data_path, "w") as f:
            f.write("""Hypertension Guidelines:
- Stage 1: BP 140-159. Treatment: Lifestyle + ACE inhibitors.
- Weather Impact: Cold weather causes blood vessels to constrict, increasing blood pressure. Monitor hypertension patients more closely in winter.

Diabetes Guidelines:
- Normal Glucose: < 100.
- Weather Impact: Extreme heat can cause dehydration, affecting blood sugar levels. Advise hydration in temperatures above 30°C.
""")

    loader = TextLoader(data_path)
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    docs = splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store.as_retriever(search_kwargs={"k": 1})

def retrieve_knowledge(query: str, retriever) -> str:
    results = retriever.invoke(query)
    return "\n".join([doc.page_content for doc in results]) if results else "No specific guidelines found."
