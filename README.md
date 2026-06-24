# GenAI Foundation Assignment - Day 1

## Overview

This assignment covers two fundamental concepts in Generative AI:
1. **Text Embeddings & Similarity Comparison** - Understanding semantic representations
2. **LLM API Integration** - Learning to interact with language models programmatically

---

## Exercise 1: Text Embeddings & Similarity Comparison

### Objective
Understand how to generate embeddings using Sentence Transformers and compute similarity between sentences.

### What it does
- Loads the **all-MiniLM-L6-v2** model from Sentence Transformers
- Converts 5 sample sentences into 384-dimensional embeddings
- Calculates cosine similarity between all pairs
- Displays first 5 dimensions of each embedding
- Creates a similarity matrix and identifies highest/lowest similarity pairs

### Key Concepts

**Embeddings**: Dense vector representations that capture semantic meaning of text
- 384 dimensions for the MiniLM model
- Similar meanings → high cosine similarity
- Different meanings → low cosine similarity

**Cosine Similarity**: Measures angle between vectors (0 to 1 scale for embeddings)
- 1.0 = identical semantics
- 0.5 = moderate semantic relationship
- 0.0 = orthogonal/unrelated

### Sample Results
```
Highest Similarity Pairs:
  S2 <-> S5: 0.5827 (AI dev + software engineers)
  S1 <-> S5: 0.5555 (GenAI + software engineers)
  S1 <-> S2: 0.5368 (GenAI + AI dev)

Lowest Similarity Pairs:
  S3 <-> S4: 0.0132 (cricket ≠ ML models) ✓
  S3 <-> S5: 0.0620 (cricket ≠ software)
  S1 <-> S3: 0.0684 (GenAI ≠ cricket)
```

### Learning Outcomes
✓ Understand embeddings as vector representations  
✓ Interpret similarity scores and semantic closeness  
✓ Use pre-trained models for text processing  
✓ Apply cosine similarity for semantic search  

### Run the script
```bash
python3 exercise1_embeddings.py
```

---

## Exercise 2: Calling LLM via API

### Objective
Learn how to interact with an LLM using an API endpoint and process responses.

### What it does
- Sends 3 different queries to the Anthropic Claude API
- Demonstrates different temperature parameters (0.5, 0.7, 0.9)
- Extracts and displays full JSON responses
- Compares responses with different parameters
- Handles authentication errors gracefully with fallback to demo mode
- Accepts dynamic user input for custom queries

### Key Concepts

**API Parameters**:
- **temperature**: Controls randomness (0.0 = deterministic, 1.0+ = creative)
  - Low temp (0.5) → focused, consistent responses
  - High temp (0.9) → varied, creative responses
- **max_tokens**: Maximum length of response
- **model**: Which LLM to use (claude-3-5-haiku-20241022)

**Response Structure**:
```json
{
  "content": [{"type": "text", "text": "assistant reply"}],
  "usage": {
    "input_tokens": 15,
    "output_tokens": 120
  }
}
```

### Query Demonstrations

**Query 1**: "What are the key benefits of using embeddings in machine learning?"
- Temperature: 0.7 (balanced)
- Focuses on practical ML benefits

**Query 2**: "Explain how cosine similarity works..."
- Temperature: 0.9 (more creative)
- Deeper technical explanation

**Query 3**: User input with dynamic question
- Temperature: 0.5 (deterministic)
- Customizable for any topic

### Error Handling
- Validates API key from `.env`
- Gracefully handles authentication errors
- Falls back to demo mode with realistic mock responses
- Provides informative error messages

### Learning Outcomes
✓ Understand API-based LLM interaction  
✓ Learn prompt structuring  
✓ Parse and extract information from JSON responses  
✓ Handle API errors and implement fallbacks  
✓ Understand temperature and model parameters  
✓ Compare responses from different configurations  

### Run the script
```bash
# Interactive mode
python3 exercise2_llm_api.py

# Non-interactive (accepts empty input)
echo "" | python3 exercise2_llm_api.py
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Install Dependencies
```bash
pip install --user --break-system-packages -r requirements.txt
```

Or create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Configuration
Create a `.env` file with your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

To get an API key:
1. Visit https://console.anthropic.com
2. Create an account or login
3. Navigate to API keys
4. Create a new key
5. Copy it to your `.env` file

---

## Key Takeaways

### Embeddings (Exercise 1)
- Embeddings transform text into numerical vectors
- Semantic meaning is preserved in the vector space
- Cosine similarity effectively measures text similarity
- Pre-trained models provide good general-purpose embeddings

### LLM APIs (Exercise 2)
- LLMs are accessed through REST APIs with structured requests/responses
- Temperature parameter controls response creativity vs consistency
- JSON parsing is essential for programmatic LLM interaction
- Error handling and fallbacks improve robustness

### Combined Learning
- Embeddings enable semantic search with LLMs
- Temperature tuning improves response quality for specific tasks
- Error handling and demo modes make applications resilient

---

## Files Structure
```
.
├── exercise1_embeddings.py      # Text embeddings & similarity
├── exercise2_llm_api.py         # LLM API interaction
├── requirements.txt              # Python dependencies
├── .env                          # API configuration
└── README.md                     # This file
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'sentence_transformers'"
- Install dependencies: `pip install --user --break-system-packages -r requirements.txt`
- Or use virtual environment

### "Invalid x-api-key" error
- Check `.env` file has correct API key format
- Verify key is valid at https://console.anthropic.com
- Script will fall back to demo mode automatically

### Model download takes too long
- Sentence Transformers downloads ~120MB model first run only
- Set `HF_TOKEN` environment variable for faster downloads
- Subsequent runs use cached model

### Connection timeout on API calls
- Check internet connection
- Verify API endpoint is accessible
- Check Anthropic API status page

---

## Additional Resources

### Sentence Transformers
- Documentation: https://www.sbert.net/
- Model Cards: https://huggingface.co/sentence-transformers
- GitHub: https://github.com/UKPLab/sentence-transformers

### Anthropic Claude API
- Documentation: https://docs.anthropic.com
- API Reference: https://docs.anthropic.com/messages/api
- Pricing: https://www.anthropic.com/pricing

### Embeddings & Semantic Search
- OpenAI Embeddings Guide: https://platform.openai.com/docs/guides/embeddings
- Cosine Similarity: https://en.wikipedia.org/wiki/Cosine_similarity
- Vector Databases: Pinecone, Weaviate, Milvus

---

## Next Steps

### Extend Exercise 1
- Try other models (all-mpnet-base-v2 for higher quality)
- Build a semantic search engine
- Cluster sentences by similarity
- Visualize embeddings with t-SNE or UMAP

### Extend Exercise 2
- Build a chatbot with conversation history
- Implement RAG (Retrieval-Augmented Generation)
- Stream responses for better UX
- Add cost tracking with token counting
- Create a prompt template system

### Combine Both Exercises
- Build a semantic search system with LLM
- Create an embeddings-based recommendation system
- Develop a multi-turn chatbot with semantic context

---

## Notes

- Demo mode activates automatically on authentication errors
- Mock responses are contextually matched to queries
- All code includes error handling and informative logging
- Scripts are designed for learning and experimentation
- Production use requires additional security measures

---

Generated: 2026-06-24
