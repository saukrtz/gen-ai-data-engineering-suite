import pandas as pd
from datetime import datetime, timedelta
import random

data = []

for i in range(20):
    data.append({
        "table_name": f"table_{i}",
        "description": "Contains customer PII" if i % 3 == 0 else "Contains transaction data",
        "columns": "id, name, email, phone" if i % 3 == 0 else "id, amount, timestamp",
        "last_updated": str(datetime.now() - timedelta(days=random.randint(1,10)))
    })

df = pd.DataFrame(data)
df.to_csv("data_catalog.csv", index=False)

print("Created data_catalog.csv successfully!")

# --- Naïve RAG Baseline ---
# Step 1: Load Data
from langchain_community.document_loaders import CSVLoader

print("\nLoading data from data_catalog.csv...")
loader = CSVLoader("data_catalog.csv")
docs = loader.load()
print(f"Loaded {len(docs)} documents.")

# Step 2: Chunk Documents
from langchain_text_splitters import CharacterTextSplitter

print("\nChunking documents...")
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"Created {len(chunks)} chunks.")

# Step 3: Create Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

print("\nInitializing Embedding Model...")
# Using HuggingFace local embeddings instead of OpenAI to prevent API key errors
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("HuggingFace Embeddings initialized.")

# Step 4: Store in FAISS
from langchain_community.vectorstores import FAISS

print("\nGenerating and storing embeddings in FAISS vector database...")
db = FAISS.from_documents(chunks, embeddings)
print("Successfully stored in FAISS database (db).")

# Step 5 & 6: Query System and Generate Answer
import os
from langchain_groq import ChatGroq

print("\nInitializing Llama model for inference...")
api_key = os.environ.get("llama_key") or os.environ.get("GROQ_API_KEY")
llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=api_key)

test_queries = [
    "Which tables contain customer PII?",
    "Show recently updated tables"
]

print("\n--- Testing Naïve RAG ---")
for q in test_queries:
    print(f"\n==========================================")
    print(f"Query: '{q}'")
    
    # 1. Retrieve
    results = db.similarity_search(q, k=3)
    context = "\n\n".join([r.page_content for r in results])
    
    # 2. Generate
    prompt = f"Answer the question strictly based on the provided Context.\n\nContext:\n{context}\n\nQuestion: {q}\nAnswer:"
    response = llm.invoke(prompt)
    
    print("\n--- LLM Final Answer ---")
    print(response.content)
