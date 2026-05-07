import os
import pandas as pd
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from rank_bm25 import BM25Okapi
from langchain_groq import ChatGroq

# 1. Load and Chunk Data
print("Loading and Chunking data from data_catalog.csv...")
loader = CSVLoader("data_catalog.csv")
docs = loader.load()
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 2. Prepare BM25
print("Initializing BM25...")
texts = [doc.page_content for doc in chunks]
tokenized = [t.split() for t in texts]
bm25 = BM25Okapi(tokenized)

# 3. Prepare FAISS Vector Store
print("Initializing FAISS Vector Store...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(chunks, embeddings)

# 4. Initialize LLM
api_key = os.environ.get("llama_key") or os.environ.get("GROQ_API_KEY")
llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=api_key)

# 5. Run Test Queries
test_queries = ["customer PII tables", "tables with email column"]

print("\n--- Running Hybrid RAG Tests ---")
for query in test_queries:
    print(f"\n==========================================")
    print(f"Query: '{query}'")
    
    # Keyword Search (BM25)
    tokenized_query = query.split()
    bm25_scores = bm25.get_scores(tokenized_query)
    top_n_bm25 = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:3]
    bm25_results = [chunks[i] for i in top_n_bm25]

    # Vector Search (FAISS)
    vector_results = db.similarity_search(query, k=3)

    # Combine Results
    combined_results = bm25_results + vector_results
    
    # Generate Answer
    context = "\n\n".join([r.page_content for r in combined_results])
    response = llm.invoke(f"Answer the question based on the following context:\n{context}\nQuestion: {query}")
    
    print("\nLLM Response:")
    print(response.content)
