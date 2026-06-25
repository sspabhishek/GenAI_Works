# GenAI Knowledge Assistant

A Flask-based web application that demonstrates RAG (Retrieval-Augmented Generation) for answering GenAI-related questions. The system retrieves relevant knowledge from ChromaDB and uses Claude API to generate beginner-friendly answers.

## Features

✅ **RAG Pipeline**: Question → Embedding → Retrieval → LLM Generation  
✅ **ChromaDB Integration**: Persistent vector database with sample GenAI knowledge  
✅ **SentenceTransformer**: Efficient text embeddings (all-MiniLM-L6-v2)  
✅ **Claude API Integration**: Production-ready LLM integration  
✅ **Beautiful UI**: Modern, responsive interface with real-time feedback  
✅ **Error Handling**: Comprehensive error handling for API and configuration issues  
✅ **Context Display**: Shows retrieved documents and similarity scores  

## Project Structure

```
GenAI_Foundation_Assignment_Day2/
├── app.py                  # Flask application & RAG logic
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── .env.example           # Example environment configuration
├── README.md              # This file
├── templates/
│   └── index.html         # Web interface
├── static/
│   └── style.css          # Styling
└── chroma_db/             # ChromaDB persistent storage (auto-created)
```

## Requirements

- Python 3.8+
- Flask 2.3.3
- SentenceTransformer 2.2.2
- ChromaDB 0.4.10
- Requests 2.31.0
- Anthropic API key

## Installation

### 1. Clone or Navigate to Project

```bash
cd GenAI_Foundation_Assignment_Day2
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and add your Anthropic API key:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
LLM_ENDPOINT=https://api.anthropic.com/v1/messages
LLM_MODEL=claude-3-5-sonnet-20241022
FLASK_ENV=development
DEBUG=True
```

**Where to get your API key:**
- Visit https://console.anthropic.com/
- Go to Settings → API Keys
- Create a new API key
- Copy and paste it into `.env`

### 5. Run the Application

```bash
python app.py
```

The app will start at `http://localhost:5000`

## How It Works

### RAG Flow

1. **User Input**: User asks a question via the web form
2. **Embedding**: Question is converted to vector embedding using SentenceTransformer
3. **Retrieval**: ChromaDB searches for top-3 similar documents using cosine similarity
4. **Context Preparation**: Retrieved documents are formatted with the question
5. **LLM Generation**: Claude API generates a beginner-friendly answer
6. **Display**: Results show question, retrieved context, similarity scores, and answer

### API Endpoints

#### POST /ask
Handles user questions and returns generated answers.

**Request:**
```json
{
  "question": "What is embeddings?"
}
```

**Response:**
```json
{
  "success": true,
  "question": "What is embeddings?",
  "answer": "Embeddings are numerical representations...",
  "context": [
    {
      "text": "Embeddings are numerical representations of text...",
      "distance": 0.1234,
      "similarity": 0.8766,
      "topic": "embeddings"
    }
  ]
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "documents_in_db": 10
}
```

## Sample Questions to Try

The knowledge base includes content about:
- **Embeddings**: Word embeddings, sentence embeddings, SentenceTransformer
- **RAG**: Retrieval-Augmented Generation, how it works
- **Transformers**: Attention mechanisms, architecture
- **Vector Databases**: ChromaDB, similarity search
- **LLMs**: Large Language Models, training, inference

### Example Queries
```
"What is embeddings?"
"How does RAG work?"
"What are transformers?"
"What is a vector database?"
"What is an LLM?"
"Difference between word and sentence embeddings"
"How to use ChromaDB?"
```

## Error Handling

The system handles these error scenarios:

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check ANTHROPIC_API_KEY in .env |
| 404 Not Found | Wrong endpoint or model | Verify LLM_ENDPOINT and LLM_MODEL |
| 405 Method Not Allowed | Wrong HTTP method | Internal issue (report if persists) |
| Timeout | LLM taking too long | Try again or check API status |
| Connection Error | Cannot reach API | Check internet connection |

## Key Components

### app.py - Main Application

**initialize_knowledge_base()**
- Loads 10 sample GenAI knowledge chunks into ChromaDB
- Automatically skips if database already initialized
- Each chunk covers different GenAI topics

**retrieve_context(query, top_k=3)**
- Queries ChromaDB for similar documents
- Returns top-k results with distance/similarity scores
- Formats metadata (topic information)

**call_llm(prompt)**
- Calls Claude API with prepared prompt
- Handles authentication and HTTP errors
- Includes system message for beginner-friendly responses
- Returns structured error messages

**prepare_prompt(question, context_docs)**
- Formats context and question into a structured prompt
- Provides clear instructions for the LLM
- Ensures consistent, focused answers

### index.html - Web Interface

- Clean, modern form for question input
- Real-time loading indicators
- Displays all three retrieved documents
- Shows similarity/distance metrics
- Beautiful answer presentation
- Responsive design for mobile devices

### style.css - Styling

- Gradient backgrounds and modern aesthetics
- Smooth animations and transitions
- Mobile-responsive grid layout
- Accessibility-focused design

## Customization

### Add More Knowledge

Edit the `knowledge_chunks` list in `app.py`:

```python
knowledge_chunks = [
    {
        "id": "topic_1",
        "text": "Your custom knowledge here...",
        "topic": "custom_topic"
    },
    # Add more chunks
]
```

Then delete `chroma_db` folder to reset and reinitialize.

### Change LLM Behavior

Edit the system message in `call_llm()`:

```python
"system": "Your custom system prompt here..."
```

### Adjust Retrieval

Change `top_k` parameter in `/ask` route:

```python
context_docs = retrieve_context(question, top_k=5)  # Get top-5 instead of top-3
```

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### ChromaDB connection issues
- Delete `chroma_db/` folder
- Restart the application
- The database will auto-initialize

### Slow embeddings on first run
- SentenceTransformer downloads model on first use (~70MB)
- Subsequent runs will be faster (uses cache)

### LLM API errors
- Verify API key is valid and active
- Check API endpoint and model name
- Ensure account has sufficient credits
- Check API rate limits

## Dependencies Explained

| Package | Purpose |
|---------|---------|
| **flask** | Web framework for HTTP routing |
| **python-dotenv** | Load environment variables from .env |
| **requests** | HTTP client for LLM API calls |
| **sentence-transformers** | Create text embeddings |
| **chromadb** | Vector database for similarity search |
| **numpy** | Numerical operations (used by transformers) |

## Performance Notes

- **First run**: ~30 seconds (SentenceTransformer model download)
- **Embedding generation**: ~100ms per query
- **ChromaDB retrieval**: ~10ms (in-memory)
- **LLM API call**: ~2-5 seconds (depends on API)
- **Total response time**: ~3-8 seconds typical

## Security Considerations

✅ API keys stored in `.env` (not hardcoded)  
✅ Input validation on all endpoints  
✅ Proper error handling without exposing internals  
✅ CORS support ready (can be added if needed)  
✅ Uses HTTPS for API calls  

⚠️ **Important**: Never commit `.env` file to git. Add to `.gitignore`:
```
.env
chroma_db/
__pycache__/
venv/
*.pyc
```

## License

Educational project for GenAI foundation learning.

## Support

For issues or questions, check:
- Anthropic API docs: https://docs.anthropic.com/
- ChromaDB docs: https://docs.trychroma.com/
- SentenceTransformer docs: https://www.sbert.net/

---

**Built for learning GenAI concepts through practical implementation.** 🚀
