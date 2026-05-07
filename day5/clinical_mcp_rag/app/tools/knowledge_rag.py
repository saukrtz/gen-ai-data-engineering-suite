import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Step 2: Unstructured Data Ingestion (RAG Pipeline)
def create_guideline_file():
    content = """Hypertension:
- BP > 140 indicates Stage 1 Hypertension
- Treatment:
  • Lifestyle changes (diet, exercise)
  • ACE inhibitors or beta blockers

Prehypertension:
- BP between 120–139
- Monitor regularly

Normal BP:
- BP < 120
- Maintain healthy lifestyle"""
    
    data_path = os.path.join(os.path.dirname(__file__), "../../guidelines.txt")
    with open(data_path, "w") as f:
        f.write(content)
    return data_path

def setup_rag():
    guideline_file = create_guideline_file()
    loader = TextLoader(guideline_file)
    documents = loader.load()
    
    splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=20)
    docs = splitter.split_documents(documents)
    
    # Using local embeddings for stability
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store.as_retriever(search_kwargs={"k": 1})

def retrieve_guidelines(query: str, retriever) -> str:
    results = retriever.invoke(query)
    if results:
        return "\n".join([doc.page_content for doc in results])
    return "No relevant guidelines found."

if __name__ == "__main__":
    retriever = setup_rag()
    print("RAG Setup Complete. Test retrieval:")
    print(retrieve_guidelines("Treatment for BP 150", retriever))
