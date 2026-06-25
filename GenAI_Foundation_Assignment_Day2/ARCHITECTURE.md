# GenAI Knowledge Assistant - Architecture Guide

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         HTML Form + Results Display                 │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │  Input: "What is embeddings?"                 │  │   │
│  │  │  Button: Ask                                  │  │   │
│  │  │  Display: Question, Context, Answer           │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP POST /ask
                           │ {question: "..."}
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              FLASK WEB APPLICATION                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Route Handler: /ask                               │   │
│  │  1. Receive user question                          │   │
│  │  2. Validate input                                 │   │
│  │  3. Call RAG Pipeline                              │   │
│  │  4. Return JSON response                           │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
┌─────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  EMBEDDINGS     │ │  CONTEXT         │ │  LLM INTEGRATION │
│  MODULE         │ │  RETRIEVAL       │ │  MODULE          │
├─────────────────┤ ├──────────────────┤ ├──────────────────┤
│                 │ │                  │ │                  │
│ • SentenceXF    │ │ • ChromaDB Query │ │ • Anthropic API  │
│ • Convert Q->V  │ │ • Similarity     │ │ • Prompt Builder │
│ • all-MiniLM    │ │   Search         │ │ • Error Handler  │
│   Model         │ │ • Cosine Dist    │ │ • Response Parse │
│                 │ │ • Top-3 Results  │ │                  │
│                 │ │ • Metadata       │ │                  │
│                 │ │                  │ │                  │
└────────┬────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
         ┌───────────────────┴────────────────────┐
         ▼                                        ▼
    ┌────────────┐                          ┌─────────────────┐
    │ CHROMADB   │                          │ ANTHROPIC API   │
    │ (Local)    │                          │ (Cloud)         │
    │ ┌────────┐ │                          │                 │
    │ │Vector  │ │                          │ Endpoint:       │
    │ │Store   │ │                          │ api.anthropic.  │
    │ │10 Docs │ │                          │ com/v1/messages │
    │ │Indexed │ │                          │                 │
    │ └────────┘ │                          │ Model:          │
    │            │                          │ claude-3-5-     │
    │ chroma_db/ │                          │ sonnet-20241022 │
    └────────────┘                          └─────────────────┘
```

---

## Data Flow Diagram

```
USER INPUT
    │
    │ "What is embeddings?"
    ▼
┌─────────────────────────────────────────┐
│ 1. INPUT VALIDATION                     │
│    • Check if question is not empty     │
│    • Sanitize input                     │
│    • Log query                          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 2. EMBEDDING GENERATION                 │
│    • Convert question to vector         │
│    • Use SentenceTransformer            │
│    • Dimension: 384 (all-MiniLM)        │
│    Q = [0.12, -0.45, 0.89, ...]        │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 3. SIMILARITY SEARCH                    │
│    • Query ChromaDB collection          │
│    • Calculate cosine similarity        │
│    • Retrieve top 3 documents           │
│    • Get metadata (topic, distance)     │
│    Results:                             │
│    • Doc1: dist=0.12, topic=embeddings │
│    • Doc2: dist=0.34, topic=embeddings │
│    • Doc3: dist=0.45, topic=embeddings │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 4. CONTEXT PREPARATION                  │
│    • Format 3 retrieved documents       │
│    • Combine with user question         │
│    • Create structured prompt:          │
│                                         │
│    "Based on context, answer:          │
│     CONTEXT:                           │
│     [3 documents]                      │
│     QUESTION:                          │
│     What is embeddings?                │
│    "                                   │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 5. LLM API CALL                         │
│    • Format HTTP request                │
│    • Add authentication header          │
│    • Send to Claude API                 │
│    • Include system message             │
│    • Set max_tokens=512                 │
│    • Wait for response                  │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 6. RESPONSE PARSING                     │
│    • Extract answer from JSON           │
│    • Handle errors (401, 404, 500)      │
│    • Format output                      │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ 7. RESPONSE FORMATTING                  │
│    • JSON response:                     │
│    {                                    │
│      "success": true,                   │
│      "question": "...",                 │
│      "answer": "...",                   │
│      "context": [                       │
│        {                                │
│          "text": "...",                 │
│          "distance": 0.12,              │
│          "similarity": 0.88,            │
│          "topic": "embeddings"          │
│        }                                │
│      ]                                  │
│    }                                    │
└────────────────┬────────────────────────┘
                 │
                 ▼
        DISPLAY IN BROWSER
```

---

## Component Details

### 1. Flask Backend (app.py)

**Responsibilities:**
- HTTP request/response handling
- RAG pipeline orchestration
- Error handling and validation
- JSON serialization

**Key Functions:**
```python
initialize_knowledge_base()     # Load data into ChromaDB
retrieve_context()              # Query similarity search
call_llm()                       # API call to Claude
prepare_prompt()                # Format prompt with context
```

**Routes:**
- `GET  /`           → Render index.html
- `POST /ask`        → Process question
- `GET  /health`     → Health check

---

### 2. Embedding Module (SentenceTransformer)

**Model:** `all-MiniLM-L6-v2`
- 384-dimensional vectors
- Sentence-level embeddings
- Pre-trained on semantic similarity
- ~70MB model size

**Process:**
```
Text → Tokenization → BERT → Mean Pooling → L2 Norm → Vector
```

**Example:**
```
"embeddings" → [-0.12, 0.45, 0.89, ...] (384 dimensions)
"RAG"         → [-0.15, 0.48, 0.91, ...] (similar)
"pizza"       → [0.82, -0.15, 0.22, ...] (very different)
```

---

### 3. Vector Database (ChromaDB)

**Configuration:**
- Collection: `genai_knowledge`
- Storage: Persistent (`chroma_db/` folder)
- Distance metric: Cosine similarity
- Index: HNSW (Hierarchical Navigable Small World)

**Data:**
```
Collection: genai_knowledge
├── Document 1: Embeddings explanation
│   ├── ID: embeddings_1
│   ├── Text: "Embeddings are numerical..."
│   ├── Metadata: {topic: "embeddings"}
│   └── Vector: [0.12, -0.45, ...]
│
├── Document 2: RAG explanation
│   ├── ID: rag_1
│   ├── Text: "RAG stands for..."
│   ├── Metadata: {topic: "rag"}
│   └── Vector: [0.15, -0.42, ...]
│
└── ... (8 more documents)
```

**Query Process:**
```
User Q → Embedding → Vector search → Cosine similarity
                              ↓
                     Distance matrix
                              ↓
                     Sort by distance
                              ↓
                     Return top 3
```

---

### 4. LLM Integration (Anthropic API)

**Request Format:**
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 512,
  "system": "You are a beginner-friendly GenAI tutor...",
  "messages": [
    {
      "role": "user",
      "content": "Based on context...\nContext:\n...\nQuestion: What is embeddings?"
    }
  ]
}
```

**Authentication:**
```
Headers:
  Content-Type: application/json
  x-api-key: sk-ant-xxxxxxx
  anthropic-version: 2023-06-01
```

**Response Format:**
```json
{
  "id": "msg_...",
  "type": "message",
  "content": [
    {
      "type": "text",
      "text": "Embeddings are numerical representations of text..."
    }
  ],
  "model": "claude-3-5-sonnet-20241022",
  "usage": {
    "input_tokens": 256,
    "output_tokens": 128
  }
}
```

---

## RAG Pipeline Detailed

```
┌──────────────────────────────────────────────────────────────┐
│         RETRIEVAL-AUGMENTED GENERATION PIPELINE             │
└──────────────────────────────────────────────────────────────┘

STAGE 1: QUERY EMBEDDING
┌─────────────────────────────┐
│ Input: "What is embeddings?"│
│          ↓                  │
│ SentenceTransformer         │
│          ↓                  │
│ Output: [0.12, -0.45, ...]  │ (384 dims)
└────────────┬────────────────┘
             │
STAGE 2: RETRIEVAL
             │
    ┌────────▼─────────┐
    │ ChromaDB Query   │
    │  ↓               │
    │ Calculate        │
    │ cosine similarity│
    │  ↓               │
    │ Top-3 by distance│
    │  ↓               │
    │ Retrieved docs:  │
    │ • Doc A (0.12)   │
    │ • Doc B (0.34)   │
    │ • Doc C (0.45)   │
    └────────┬─────────┘
             │
STAGE 3: AUGMENTATION
             │
    ┌────────▼──────────────┐
    │ Prepare Prompt        │
    │  ↓                    │
    │ Format context        │
    │  ↓                    │
    │ Add system message    │
    │  ↓                    │
    │ Formatted prompt:     │
    │ "Based on context:\n  │
    │  CONTEXT:\n           │
    │  [Doc A]\n            │
    │  [Doc B]\n            │
    │  [Doc C]\n            │
    │  QUESTION:\n          │
    │  What is embeddings?" │
    └────────┬──────────────┘
             │
STAGE 4: GENERATION
             │
    ┌────────▼──────────────┐
    │ Claude API Call       │
    │  ↓                    │
    │ Send prompt           │
    │  ↓                    │
    │ LLM generates         │
    │  ↓                    │
    │ Generated response:   │
    │ "Embeddings are       │
    │  numerical            │
    │  representations..." │
    └────────┬──────────────┘
             │
STAGE 5: FORMATTING
             │
    ┌────────▼──────────────┐
    │ Format Output         │
    │  ↓                    │
    │ Create JSON response  │
    │  ↓                    │
    │ Include metrics       │
    │  ↓                    │
    │ Display in browser    │
    └──────────────────────┘
```

---

## Error Handling Flow

```
                    ┌─────────────────┐
                    │  Request to API │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Response Status │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    ┌──────┐            ┌──────┐            ┌──────┐
    │ 200  │            │ 401  │            │ 404  │
    │ OK   │            │ Auth │            │ Not  │
    │      │            │ Fail │            │Found │
    └───┬──┘            └───┬──┘            └───┬──┘
        │                   │                   │
        ▼                   ▼                   ▼
   Process      API Key     Wrong endpoint
   response     issue       or model

        │                   │                   │
        ▼                   ▼                   ▼
   ✅ Success        ❌ Error 401        ❌ Error 404
   Return answer     Check key          Check config
```

---

## Performance Characteristics

### Timing Breakdown

```
Operation                   Time        Notes
────────────────────────────────────────────────────────
Setup
├─ Model download          ~30-60s     First run only
├─ Virtual env setup       ~2s         One time
└─ Dependencies install    ~3-5m       One time

Runtime per query
├─ Input validation        ~1ms
├─ Embedding generation    ~100ms      SentenceTransformer
├─ ChromaDB retrieval      ~10ms       In-memory + HNSW
├─ Prompt preparation      ~5ms
├─ LLM API call           2-5s        Network + Claude processing
│  ├─ Network round-trip   500-1000ms
│  ├─ API processing       1-4s
│  └─ Token generation     ~100ms per 100 tokens
├─ Response parsing        ~5ms
└─ Frontend render         ~200ms
                           ─────────────
Total per query           2.5-5.5s    Typical

Cold start (first query)
├─ Model load from disk    ~500ms
├─ Regular query           2.5-5.5s
                           ─────────────
Total                      3-6s
```

### Memory Usage

```
Component               Memory
────────────────────────────────────
SentenceTransformer    ~500MB
ChromaDB collection    ~10MB (10 docs)
Flask app              ~50MB
Python runtime         ~100MB
────────────────────────────────────
Total typical:         ~660MB

Min viable:            ~200MB
Max reasonable:        ~1GB
```

### Scalability Limits

```
Factor               Limit           Notes
────────────────────────────────────────────
Concurrent users     1-10            Limited by LLM API
ChromaDB docs        ~10k-100k       Performance degrades beyond
Context size         ~4k tokens      Depends on model
API rate limit       Varies          Per account/plan
Embedding batch      ~1k docs        Memory dependent
Response time        2-30s           Depends on LLM load
```

---

## Deployment Architecture

### Local Development
```
Developer Machine
├─ Python + venv
├─ Flask dev server
├─ ChromaDB (local file)
└─ Browser access via localhost:5000
```

### Production Deployment (Example: Heroku)
```
┌─────────────────────────────────┐
│     Client Browser              │
└────────────┬────────────────────┘
             │ HTTPS
             ▼
┌─────────────────────────────────┐
│   Load Balancer / Reverse Proxy │
│   (Nginx / Heroku Router)       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Flask Dynos (scaled)          │
│   ├─ Web dyno 1                │
│   ├─ Web dyno 2                │
│   └─ Web dyno 3                │
└────────────┬────────────────────┘
             │
       ┌─────┴─────┐
       ▼           ▼
  ┌────────┐  ┌──────────┐
  │ChromaDB│  │ Anthropic│
  │   DB   │  │   API    │
  │(S3)    │  │ (Cloud)  │
  └────────┘  └──────────┘
```

---

## Security Architecture

```
┌──────────────────────────────────────────┐
│         SECURITY LAYERS                  │
└──────────────────────────────────────────┘

Layer 1: Secrets Management
    ├─ .env file (local only)
    ├─ Environment variables
    └─ API keys NOT in code

Layer 2: Input Validation
    ├─ Question length check
    ├─ Sanitization
    └─ Type validation

Layer 3: API Security
    ├─ x-api-key authentication
    ├─ HTTPS/TLS encryption
    └─ Request signing

Layer 4: Error Handling
    ├─ No internal errors exposed
    ├─ Generic error messages
    └─ Detailed logging

Layer 5: Rate Limiting
    ├─ API quota enforcement
    ├─ Request throttling
    └─ Cost control
```

---

## Configuration Management

```
Configuration Hierarchy
      (Lower → Higher Priority)
            │
            ▼
   1. Code defaults
            │
            ▼
   2. Config files (config.py)
            │
            ▼
   3. .env file
            │
            ▼
   4. Environment variables
            │
            ▼
   5. Runtime parameters
```

---

## Technology Stack

```
Frontend
├─ HTML5 (semantic markup)
├─ CSS3 (responsive design)
└─ Vanilla JS (no frameworks)

Backend
├─ Python 3.8+
├─ Flask (minimal web framework)
├─ requests (HTTP client)
└─ python-dotenv (config)

AI/ML
├─ SentenceTransformer (embeddings)
├─ ChromaDB (vector DB)
└─ Anthropic Claude (LLM)

Infrastructure
├─ Local filesystem (ChromaDB storage)
├─ REST API (communication)
└─ HTTP/HTTPS (protocol)
```

---

## Conclusion

This architecture demonstrates:
- ✅ Clean separation of concerns
- ✅ RAG pattern implementation
- ✅ Scalable vector database usage
- ✅ Secure API integration
- ✅ Production-ready error handling
- ✅ Minimal but complete stack

**Key Design Principles:**
- **Simplicity**: No unnecessary complexity
- **Modularity**: Independent components
- **Robustness**: Comprehensive error handling
- **Scalability**: Ready to grow
- **Security**: Secrets management
