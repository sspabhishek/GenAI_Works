# Complete Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for downloading dependencies and API calls)
- Anthropic API key

---

## Step-by-Step Installation

### Step 1: Get Anthropic API Key (Required)

1. Visit: https://console.anthropic.com/
2. Sign in or create a free account
3. Go to **Settings** → **API Keys**
4. Click **Create Key** button
5. Copy the API key (starts with `sk-ant-`)
6. Keep it safe - you'll need it in Step 4

**⏱️ Time: 2 minutes**

---

### Step 2: Prepare Project Directory

The project is already in:
```
~/Desktop/GenAI_Foundation_Assignment_Day2/
```

Navigate to it:
```bash
cd ~/Desktop/GenAI_Foundation_Assignment_Day2
```

**⏱️ Time: 30 seconds**

---

### Step 3: Create Virtual Environment

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### On Windows (Command Prompt):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

You should see `(venv)` in your terminal prompt after activation.

**⏱️ Time: 1-2 minutes**

---

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- python-dotenv (environment variables)
- requests (HTTP client)
- sentence-transformers (embeddings)
- chromadb (vector database)
- numpy (numerical computing)

**⏱️ Time: 3-5 minutes** (depends on internet speed)

---

### Step 5: Configure Environment Variables

Open the `.env` file in your editor:

**Linux/macOS:**
```bash
nano .env
# or
vim .env
```

**Windows (Notepad):**
```cmd
notepad .env
```

**VS Code (all platforms):**
```bash
code .env
```

**Edit the file:**

Replace:
```
ANTHROPIC_API_KEY=your_api_key_here
```

With your actual API key (from Step 1):
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
```

Save the file. (**Ctrl+S** or **Cmd+S**)

**⏱️ Time: 2 minutes**

---

### Step 6: Verify Installation (Optional but Recommended)

```bash
python check_config.py
```

This will check:
- ✅ Python version
- ✅ All dependencies installed
- ✅ .env file configured
- ✅ All files present
- ✅ API connectivity

Expected output:
```
==================================================
GenAI Knowledge Assistant - Configuration Check
==================================================

✅ Python 3.9.15
  ✅ Flask
  ✅ python-dotenv
  ✅ requests
  ✅ SentenceTransformer
  ✅ ChromaDB
  ✅ NumPy

...

==================================================
SUMMARY
==================================================
✅ PASS: Python Version
✅ PASS: Dependencies
✅ PASS: Folders
✅ PASS: Files
✅ PASS: .env File
✅ PASS: API Connection

==================================================
✅ All checks passed! Ready to run:

   python app.py
==================================================
```

**⏱️ Time: 1-2 minutes**

---

### Step 7: Run the Application

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Initializing knowledge base with 10 documents
```

**⏱️ Time: 30 seconds**

---

### Step 8: Open in Browser

1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the GenAI Knowledge Assistant interface

---

## 🧪 Test the Application

### First Query (Recommended)

**Type in the question box:**
```
What is embeddings?
```

**Click:** Ask

**Expected:**
- ⏳ Loading spinner appears (3-8 seconds)
- 📚 Shows 3 retrieved documents with similarity scores
- 💡 Shows AI-generated answer
- ✨ Display updates smoothly

---

### More Test Queries

Try any of these:
```
How does RAG work?
What are transformers?
What is a vector database?
What is an LLM?
Explain attention mechanisms
How to create embeddings?
```

---

## ⚠️ Troubleshooting

### Problem: "Module not found" Error

**Error message:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Ensure virtual environment is activated (you should see (venv) in prompt)
pip install -r requirements.txt
```

---

### Problem: "API key not configured" Error

**Error message in browser:**
```
Error: ANTHROPIC_API_KEY not configured in .env
```

**Solution:**
1. Open `.env` file
2. Replace `your_api_key_here` with your actual API key
3. Save the file
4. Refresh browser (Ctrl+R or Cmd+R)
5. Try again

**Verify:**
```bash
python check_config.py
```

---

### Problem: "Connection Error" or API Fails

**Error message:**
```
Error: Could not connect to LLM endpoint
```

**Checklist:**
- ✅ Internet connection working
- ✅ API key is valid (test on https://console.anthropic.com/)
- ✅ API key has sufficient credits
- ✅ LLM_ENDPOINT is correct: `https://api.anthropic.com/v1/messages`
- ✅ LLM_MODEL is valid: `claude-3-5-sonnet-20241022`

---

### Problem: "Port 5000 already in use"

**Error message:**
```
OSError: [Errno 48] Address already in use
```

**Solution:** Change the port in `app.py`, line 281:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

Then access: `http://localhost:5001`

---

### Problem: First Run is Slow

**Why:** SentenceTransformer downloads ML model (~70MB) on first run. This is normal.

**Time:** ~30-60 seconds for first download

**After:** Subsequent runs are fast (the model is cached)

---

### Problem: "File not found" errors

**Make sure you're in the right directory:**
```bash
pwd  # Check current directory
ls   # Should show: app.py, requirements.txt, templates, static, etc.
```

**Should output:**
```
~/Desktop/GenAI_Foundation_Assignment_Day2
```

---

## 🚀 What Happens After Setup

### Knowledge Base Initialization
- 10 knowledge chunks are automatically loaded into ChromaDB
- Located in `chroma_db/` folder (created automatically)
- Persists between sessions

### On Each Query
1. Your question is converted to numbers (embeddings)
2. System searches ChromaDB for similar documents
3. Top 3 documents are retrieved
4. Context + question sent to Claude API
5. Answer displayed with similarity scores

### Total Response Time
- **First time**: ~8-12 seconds (API warming up)
- **Typical**: ~3-5 seconds
- **After cache**: ~2-3 seconds

---

## 📁 Project Structure After Setup

```
GenAI_Foundation_Assignment_Day2/
├── venv/                   # Virtual environment (auto-created)
│   ├── bin/               # Executables
│   ├── lib/               # Packages
│   └── ...
├── chroma_db/             # ChromaDB database (auto-created on first run)
│   ├── chroma.db
│   └── ...
├── templates/
│   └── index.html         # Web interface
├── static/
│   └── style.css          # Styling
├── app.py                 # Main application
├── requirements.txt       # Dependencies list
├── .env                   # Your API configuration
├── .env.example          # Example configuration
├── README.md             # Full documentation
├── QUICKSTART.md         # Quick start guide
├── INSTALL.md            # This file
├── PROJECT_SUMMARY.md    # Project overview
└── check_config.py       # Configuration checker
```

---

## 🔒 Security Notes

### API Key Safety
- ✅ Store API key only in `.env`
- ✅ Never commit `.env` to git
- ✅ `.gitignore` already configured to protect it
- ❌ Don't hardcode API keys in code
- ❌ Don't share your `.env` file

### Rate Limiting
- Anthropic API has rate limits (depends on your plan)
- Each query costs a small amount
- Monitor usage at: https://console.anthropic.com/

---

## 🎓 After Installation

### Next Steps

1. **Explore the Code**
   - Read `app.py` to understand the RAG pipeline
   - See how embeddings and retrieval work
   - Learn about prompt engineering

2. **Customize**
   - Add more knowledge chunks
   - Change the system prompt
   - Modify the UI styling

3. **Extend**
   - Add conversation history
   - Implement user feedback
   - Add more domains of knowledge

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Got Anthropic API key
- [ ] Navigated to project directory
- [ ] Created virtual environment
- [ ] Activated virtual environment (`(venv)` in prompt)
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Added API key to `.env` file
- [ ] Ran configuration check (`python check_config.py`)
- [ ] Started Flask app (`python app.py`)
- [ ] Opened browser to `http://localhost:5000`
- [ ] Tested with sample query
- [ ] Got answer back successfully

**If all checked: ✅ You're done!**

---

## 💬 Getting Help

### Common Questions

**Q: Do I need to pay for this?**
A: Anthropic API calls are paid, but there's a free tier. Check pricing at console.anthropic.com

**Q: Can I use a different LLM?**
A: Yes, modify `LLM_ENDPOINT` and `LLM_MODEL` in `.env`

**Q: How do I stop the app?**
A: Press `Ctrl+C` in the terminal

**Q: Can I run on a different port?**
A: Yes, edit line 281 in `app.py` to change the port

**Q: How do I add more knowledge?**
A: Edit `knowledge_chunks` list in `app.py` and restart

---

## 📚 Resources

- **Anthropic Docs**: https://docs.anthropic.com/
- **ChromaDB Docs**: https://docs.trychroma.com/
- **SentenceTransformer**: https://www.sbert.net/
- **Flask Docs**: https://flask.palletsprojects.com/

---

## ✨ You're All Set!

Your GenAI Knowledge Assistant is ready to use. 

**Start the app:**
```bash
python app.py
```

**Then visit:**
```
http://localhost:5000
```

**Happy learning!** 🚀

---

**Need help?** Check README.md for detailed documentation.
