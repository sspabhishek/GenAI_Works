import os
import json
import chromadb
import requests
import numpy as np
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
CHROMA_DB_PATH = "./chroma_db"
API_KEY = os.getenv("ANTHROPIC_API_KEY")
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT")
LLM_MODEL = os.getenv("LLM_MODEL")

# Ensure ChromaDB path exists
os.makedirs(CHROMA_DB_PATH, exist_ok=True)

# Initialize ChromaDB client with persistent storage
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Initialize SentenceTransformer for embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name="genai_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def initialize_knowledge_base():
    """Load sample GenAI knowledge chunks into ChromaDB"""

    # Sample knowledge chunks
    knowledge_chunks = [
        {
            "id": "embeddings_1",
            "text": "Embeddings are numerical representations of text that capture meaning. They convert words or documents into vectors of numbers that machine learning models can understand. For example, 'king' and 'queen' have similar embeddings because they represent similar concepts. Embeddings are created by neural networks trained on large amounts of text data.",
            "topic": "embeddings"
        },
        {
            "id": "embeddings_2",
            "text": "Word embeddings like Word2Vec and GloVe represent individual words as vectors. Sentence embeddings represent entire sentences or documents. Popular models for creating embeddings include SentenceTransformer, which uses BERT and other transformer architectures. These models can be pre-trained on massive datasets like Wikipedia and books.",
            "topic": "embeddings"
        },
        {
            "id": "rag_1",
            "text": "RAG stands for Retrieval-Augmented Generation. It's a technique that combines searching for relevant information with generating new text. First, the system retrieves relevant documents from a database, then uses those documents as context when generating an answer. This helps AI models provide more accurate and factual responses.",
            "topic": "rag"
        },
        {
            "id": "rag_2",
            "text": "RAG workflow: 1) Convert user question to embedding, 2) Search vector database for similar documents, 3) Retrieve top-k relevant documents, 4) Create a prompt with retrieved context and user question, 5) Send to LLM for answer generation. This approach reduces hallucinations and ensures answers are grounded in actual knowledge.",
            "topic": "rag"
        },
        {
            "id": "transformers_1",
            "text": "Transformers are a type of neural network architecture that excel at processing sequential data like text. They use 'attention mechanisms' to understand relationships between words, even if they're far apart in the text. Popular transformer models include BERT, GPT, and T5. They're the foundation of modern large language models.",
            "topic": "transformers"
        },
        {
            "id": "transformers_2",
            "text": "The attention mechanism in transformers allows each word to 'attend to' or focus on other words in the input. This helps the model understand context and relationships. Unlike older RNN models that process text sequentially, transformers can process all words in parallel, making them faster to train and more efficient.",
            "topic": "transformers"
        },
        {
            "id": "vector_db_1",
            "text": "Vector databases like ChromaDB, Pinecone, and Weaviate store and search high-dimensional embeddings efficiently. They use specialized algorithms like HNSW (Hierarchical Navigable Small World) for fast similarity search. Vector databases are essential for RAG systems because they enable quick retrieval of similar documents.",
            "topic": "vector_databases"
        },
        {
            "id": "vector_db_2",
            "text": "ChromaDB is an open-source vector database designed for AI developers. It can store embeddings locally or in the cloud. ChromaDB provides an easy Python API for adding documents, querying, and managing collections. It automatically handles embedding generation if you provide the documents.",
            "topic": "vector_databases"
        },
        {
            "id": "llm_1",
            "text": "Large Language Models (LLMs) like GPT and Claude are neural networks trained on billions of text examples. They can understand and generate human-like text. LLMs use transformer architecture and are trained using techniques like next-token prediction. They power applications like chatbots, content generation, and code assistants.",
            "topic": "llm"
        },
        {
            "id": "llm_2",
            "text": "LLMs work by predicting the next word in a sequence based on previous words. During training, they learn patterns in language. The model has billions of parameters (weights) that are adjusted during training. Once trained, they can be fine-tuned for specific tasks or used as-is with prompt engineering.",
            "topic": "llm"
        }
    ]

    # Check if collection already has data
    collection_count = collection.count()
    if collection_count > 0:
        print(f"Knowledge base already initialized with {collection_count} documents")
        return

    # Add documents to ChromaDB
    ids = []
    documents = []
    metadatas = []

    for chunk in knowledge_chunks:
        ids.append(chunk["id"])
        documents.append(chunk["text"])
        metadatas.append({"topic": chunk["topic"]})

    # Add to collection (ChromaDB will auto-embed using default model)
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Initialized knowledge base with {len(knowledge_chunks)} documents")


def retrieve_context(query, top_k=3):
    """Retrieve top-k relevant documents from ChromaDB"""
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        # Format results
        retrieved_docs = []
        if results and results["documents"] and len(results["documents"]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                distance = results["distances"][0][i] if results["distances"] else 0
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}

                retrieved_docs.append({
                    "text": doc,
                    "distance": float(distance),
                    "topic": metadata.get("topic", "unknown")
                })

        return retrieved_docs
    except Exception as e:
        print(f"Error retrieving context: {str(e)}")
        return []


def call_llm(prompt):
    """Call Anthropic Claude API with the prepared prompt"""

    # Validate API configuration
    if not API_KEY:
        return None, "Error: ANTHROPIC_API_KEY not configured in .env"
    if not LLM_ENDPOINT:
        return None, "Error: LLM_ENDPOINT not configured in .env"
    if not LLM_MODEL:
        return None, "Error: LLM_MODEL not configured in .env"

    try:
        headers = {
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01"
        }

        payload = {
            "model": LLM_MODEL,
            "max_tokens": 512,
            "system": "You are a beginner-friendly GenAI tutor. Explain concepts clearly and simply, avoiding jargon. Keep your answer concise and focused on the user's question.",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = requests.post(
            LLM_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )

        # Handle different HTTP status codes
        if response.status_code == 401:
            return None, "Error 401: Unauthorized - Check your ANTHROPIC_API_KEY"
        elif response.status_code == 404:
            return None, "Error 404: Endpoint/Model not found - Check LLM_ENDPOINT and LLM_MODEL"
        elif response.status_code == 405:
            return None, "Error 405: Method not allowed"
        elif response.status_code != 200:
            return None, f"Error {response.status_code}: {response.text}"

        # Extract answer from response
        response_data = response.json()
        print("Response Data : ", response_data)
        if "choices" in response_data and len(response_data["choices"]) > 0:
            answer = response_data["choices"][0]["message"]["content"]
            return answer, None
        else:
            return None, "Error: Unexpected response format from LLM"

    except requests.exceptions.Timeout:
        return None, "Error: Request to LLM timed out"
    except requests.exceptions.ConnectionError:
        return None, "Error: Could not connect to LLM endpoint"
    except Exception as e:
        return None, f"Error calling LLM: {str(e)}"


def prepare_prompt(question, context_docs):
    """Prepare prompt with context and question"""

    # Format context
    context_text = "\n---\n".join([doc["text"] for doc in context_docs])

    prompt = f"""Based on the following GenAI knowledge context, answer the user's question clearly and simply.

CONTEXT:
{context_text}

USER QUESTION:
{question}

Please provide a clear, beginner-friendly explanation. Focus on the specific question asked."""

    return prompt


@app.route("/")
def index():
    """Render the main page"""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """Handle user question and return answer with context"""

    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        # Validate input
        if not question:
            return jsonify({
                "success": False,
                "error": "Please enter a question"
            }), 400

        # Retrieve relevant context
        context_docs = retrieve_context(question, top_k=3)

        if not context_docs:
            return jsonify({
                "success": False,
                "error": "Could not retrieve relevant documents from knowledge base"
            }), 400

        # Prepare prompt
        prompt = prepare_prompt(question, context_docs)

        # Call LLM
        answer, error = call_llm(prompt)

        if error:
            return jsonify({
                "success": False,
                "error": error
            }), 500

        # Format response
        response = {
            "success": True,
            "question": question,
            "answer": answer,
            "context": [
                {
                    "text": doc["text"],
                    "distance": doc["distance"],
                    "similarity": round(1 - doc["distance"], 3),
                    "topic": doc["topic"]
                }
                for doc in context_docs
            ]
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "documents_in_db": collection.count()
    }), 200


if __name__ == "__main__":
    # Initialize knowledge base on startup
    initialize_knowledge_base()

    # Run Flask app
    app.run(debug=True, port=5000)
