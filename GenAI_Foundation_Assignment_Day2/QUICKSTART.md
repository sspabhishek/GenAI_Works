# Quick Start Guide

Get the GenAI Knowledge Assistant running in 5 minutes!

## Step 1: Get Your API Key (1 minute)

1. Go to https://console.anthropic.com/
2. Sign in or create an account
3. Click "Settings" → "API Keys"
4. Click "Create Key"
5. Copy the key (looks like: `sk-ant-...`)

## Step 2: Setup Project (2 minutes)

### On macOS/Linux:
```bash
cd GenAI_Foundation_Assignment_Day2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your API key to .env
# Edit .env file and replace 'your_api_key_here' with your actual key
nano .env
```

### On Windows:
```bash
cd GenAI_Foundation_Assignment_Day2

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Edit .env file and add your API key
# Open .env in Notepad and update the key
```

## Step 3: Run the App (30 seconds)

```bash
python app.py
```

You'll see:
```
 * Running on http://localhost:5000
 * Initialized knowledge base with 10 documents
```

## Step 4: Open in Browser (30 seconds)

1. Open your browser
2. Go to: `http://localhost:5000`
3. Type a question: "What is embeddings?"
4. Click "Ask"
5. Wait 3-5 seconds for the answer

## Try These Questions

- ✅ "What is embeddings?"
- ✅ "How does RAG work?"
- ✅ "What are transformers?"
- ✅ "What is a vector database?"
- ✅ "Explain LLMs simply"

## How It Works

```
Question
   ↓
[Convert to embedding]
   ↓
[Search ChromaDB for similar docs]
   ↓
[Get top 3 results]
   ↓
[Send to Claude with context]
   ↓
[Get AI answer]
   ↓
Display on screen
```

## Troubleshooting

### "Module not found" error?
```bash
pip install -r requirements.txt
```

### "API key not configured" error?
1. Open `.env` file
2. Replace `your_api_key_here` with your actual API key
3. Save and restart Flask

### "Connection error"?
- Check internet connection
- Verify API key is valid
- Check if Anthropic API is up (status.anthropic.com)

### App running slow?
- First run downloads ML model (~70MB) - this is normal
- Subsequent runs are fast
- LLM API calls naturally take 2-5 seconds

## File Guide

| File | Purpose |
|------|---------|
| `app.py` | Main Flask app with RAG logic |
| `.env` | Your API credentials (secret!) |
| `templates/index.html` | Web interface |
| `static/style.css` | Styling |
| `chroma_db/` | Knowledge database (auto-created) |

## What's Happening Behind the Scenes

1. **Embedding**: Your question becomes numbers that represent meaning
2. **Retrieval**: These numbers are compared with stored knowledge
3. **Context**: Top 3 similar documents are found
4. **Generation**: Claude reads the context and answers your question
5. **Display**: Results show the question, context sources, and AI answer

## Next Steps

- ✨ Modify `.env` to use different Claude models
- 📚 Add more knowledge chunks to `app.py`
- 🎨 Customize styling in `static/style.css`
- 🔍 Adjust how many documents are retrieved (change `top_k=3` in `app.py`)

## Need Help?

Check the full [README.md](README.md) for detailed documentation.

---

**You're all set! Happy learning!** 🚀
