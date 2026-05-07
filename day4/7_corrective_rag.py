import os
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from rank_bm25 import BM25Okapi
from langchain_groq import ChatGroq

print("--- CORRECTIVE RAG (CRAG) INITIALIZATION ---")

# 1. Setup Base Hybrid Retrieval
loader = CSVLoader("data_catalog.csv")
docs = loader.load()
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(chunks, embeddings)

texts = [doc.page_content for doc in chunks]
tokenized = [t.split() for t in texts]
bm25 = BM25Okapi(tokenized)

api_key = os.environ.get("llama_key") or os.environ.get("GROQ_API_KEY")
llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=api_key)

# 2. Define the Evaluator/Grader
def grade_documents(query, documents):
    print(f"\n--- Grading {len(documents)} retrieved documents for relevance ---")
    relevant_docs = []
    
    for doc in documents:
        prompt = f"""
        You are a grader evaluating the relevance of a retrieved document to a user question.
        
        Retrieved Document: {doc.page_content}
        User Question: {query}
        
        If the document contains keywords or semantic meaning related to the user question, grade it as 'RELEVANT'. 
        Otherwise, grade it as 'IRRELEVANT'.
        
        Respond with only one word: RELEVANT or IRRELEVANT.
        """
        response = llm.invoke(prompt).content.strip().upper()
        
        if "RELEVANT" in response and "IRRELEVANT" not in response:
            print(f"Result: [RELEVANT]")
            relevant_docs.append(doc)
        else:
            print(f"Result: [IRRELEVANT] - Filtering out.")
            
    return relevant_docs

# 3. Test the Corrective Pipeline
query = "tables with email column"
print(f"\nQuery: {query}")

# Base Retrieval
tokenized_query = query.split()
bm25_scores = bm25.get_scores(tokenized_query)
top_n_bm25 = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:3]
bm25_results = [chunks[i] for i in top_n_bm25]
vector_results = db.similarity_search(query, k=3)

combined_results = bm25_results + vector_results

# Step 1: Remove Duplicate Results
unique_results = list({r.page_content: r for r in combined_results}.values())

# Step 2: Re-ranking (Simple Heuristic)
def rerank(results, query):
    # Sort results based on whether the exact query string exists in the content
    return sorted(results, key=lambda x: query.lower() in x.page_content.lower(), reverse=True)

reranked = rerank(unique_results, query)

# Step 3: Filter Relevant Results
filtered = [r for r in reranked if "PII" in r.page_content or "customer" in r.page_content]

# Step 4: Generate Final Answer
if filtered:
    context = "\n".join([r.page_content for r in filtered])
    
    # Using invoke() as it's the modern equivalent of the deprecated predict()
    final_response = llm.invoke(f"Answer clearly:\n{context}\nQuestion:{query}")
    print("\n--- Final Answer ---")
    print(final_response.content)
else:
    print("\nNo relevant results found after filtering.")
