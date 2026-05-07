from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = CSVLoader("catalog.csv")
documents = loader.load()

# Optional: Print the documents to verify
# print(documents)

splitter = RecursiveCharacterTextSplitter(chunk_size=300)
chunks = splitter.split_documents(documents)

print(f"Chunks created: {len(chunks)}")

from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("HuggingFace (sentence-transformers) embedding model initialized.")

from langchain_community.vectorstores import FAISS

print("Generating embeddings and storing in FAISS vector database...")
vectorstore = FAISS.from_documents(documents=chunks, embedding=embedding_model)
print("Embeddings generated and stored in FAISS successfully!")

# --- Similarity Search ---
query = "customer PII"
print(f"\nPerforming similarity search for: '{query}'")
results = vectorstore.similarity_search(query, k=3)

for i, res in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(res.page_content)

# --- RAG Pipeline (LLM) ---
import os
from langchain_groq import ChatGroq

print("\nInitializing Llama model via Groq...")
api_key = os.environ.get("llama_key") or os.environ.get("GROQ_API_KEY")

llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=api_key)

llm_query = "Which tables contain customer PII?"
print(f"Querying LLM with RAG: '{llm_query}'\n")

# Use the context from our earlier search results (or do a new search)
context = "\n\n".join([r.page_content for r in results])

# Predict is deprecated, so we use invoke()
response = llm.invoke(f"Based on the following Context:\n{context}\n\nQuestion: {llm_query}\nAnswer:")

print("--- LLM Response ---")
print(response.content)
