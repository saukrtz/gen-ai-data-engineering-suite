from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import CharacterTextSplitter

# Step 1: Load and Chunk Data
print("Loading and Chunking data...")
loader = CSVLoader("data_catalog.csv")
docs = loader.load()
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Step 2: Prepare Text Corpus (BM25)
from rank_bm25 import BM25Okapi

print("\nPreparing Text Corpus for BM25...")
texts = [doc.page_content for doc in chunks]
tokenized = [t.split() for t in texts]

bm25 = BM25Okapi(tokenized)
print("BM25 Keyword search successfully initialized!")

# Step 3: Keyword Search
print("\n--- Running BM25 Keyword Search ---")
query = "customer PII tables"
tokenized_query = query.split()

bm25_scores = bm25.get_scores(tokenized_query)
top_n = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:3]

bm25_results = [chunks[i] for i in top_n]

for i, r in enumerate(bm25_results):
    print(f"BM25 Result {i+1}:")
    print(r.page_content)
    print(f"Score: {bm25_scores[top_n[i]]}\n")

# Step 4: Vector Search (FAISS)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("--- Running FAISS Vector Search ---")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(chunks, embeddings)

vector_results = db.similarity_search(query, k=3)

for i, r in enumerate(vector_results):
    print(f"Vector Result {i+1}:")
    print(r.page_content)
    print()

# Step 5: Combine Results
print("--- Combining Results ---")
combined_results = bm25_results + vector_results
print(f"Total combined results: {len(combined_results)}")

# Step 6: Generate Answer
import os
from langchain_groq import ChatGroq

print("\n--- Generating Answer ---")
api_key = os.environ.get("llama_key") or os.environ.get("GROQ_API_KEY")
llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=api_key)

context = "\n".join([r.page_content for r in combined_results])
response = llm.invoke(f"Answer based on the following context:\n{context}\nQuestion: {query}")
print("\nLLM Response:")
print(response.content)
