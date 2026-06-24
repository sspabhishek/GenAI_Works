#!/usr/bin/env python3
"""
Exercise 2: Calling LLM via API
Demonstrates API-based LLM interaction with dynamic input and error handling.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('ANTHROPIC_API_KEY')
print("API Key : ", API_KEY)

if not API_KEY:
    print("⚠️  WARNING: ANTHROPIC_API_KEY not found in .env file")
    print("   Using demo mode with mock responses instead\n")
    DEMO_MODE = True
else:
    DEMO_MODE = False

# API Configuration
API_URL = "https://llmgw-wp.tekstac.com/v1/chat/completions"
if not DEMO_MODE:
    HEADERS = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
else:
    HEADERS = {}

# Mock responses for demo mode
MOCK_RESPONSES = {
    "embeddings": """Embeddings are dense vector representations of text or data. Key benefits include:

1. **Semantic Understanding**: Embeddings capture the meaning of text, not just keywords
2. **Dimensionality Reduction**: Compress high-dimensional data into lower dimensions
3. **Similarity Computation**: Enable fast similarity calculations between pieces of text
4. **Transfer Learning**: Pre-trained embeddings can be reused for multiple tasks
5. **Improved Performance**: Often improve ML model accuracy by providing better features

Embeddings are fundamental to modern NLP applications and semantic search.""",

    "cosine_similarity": """Cosine similarity measures the angle between two vectors. Here's how it works:

**How it works:**
- Calculate the dot product of two vectors
- Divide by the product of their magnitudes
- Results range from -1 to 1 (typically 0 to 1 for embeddings)

**Why it's useful for embeddings:**
1. **Magnitude-Independent**: Focuses on direction, not magnitude
2. **Normalized Scale**: Always produces comparable values between -1 and 1
3. **Efficient**: Fast to compute even for high-dimensional embeddings
4. **Interpretable**: 1.0 = identical, 0.0 = orthogonal, -1.0 = opposite
5. **Effective for Semantic Search**: Excellent for finding similar documents/sentences

Example: Two sentences about "cats" will have high cosine similarity despite different lengths.""",

    "generative_ai": """Generative AI vs Traditional Machine Learning:

**Generative AI:**
- Creates new data (text, images, code, etc.)
- Uses large language models and neural networks
- Can generate human-like responses and content
- Examples: ChatGPT, DALL-E, Copilot
- Better at understanding context and nuance

**Traditional ML:**
- Predicts or classifies existing data
- Uses structured algorithms (decision trees, SVM, etc.)
- Requires labeled training data
- Examples: Linear regression, random forests
- Better for structured, well-defined tasks

**Key Difference:** Traditional ML learns patterns from data to predict; Generative AI learns patterns to create new data."""
}

print("=" * 70)
print("Exercise 2: Calling LLM via API")
print("=" * 70)

def send_llm_request(prompt, temperature=0.7, max_tokens=300, force_demo=False):
    """Send a request to the LLM API and return the response."""
    payload = {
        "model": "global.anthropic.claude-haiku-4-5-20251001-v1:0",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        print(f"\n[*] Sending request to LLM API...")
        print(f"    Model: {payload['model']}")
        print(f"    Temperature: {temperature}")
        print(f"    Max Tokens: {max_tokens}")

        if DEMO_MODE or force_demo:
            print(f"    [DEMO MODE - Using mock response]\n")
            # Determine which mock response to use
            if "embedding" in prompt.lower():
                mock_reply = MOCK_RESPONSES["embeddings"]
            elif "cosine" in prompt.lower() or "similarity" in prompt.lower():
                mock_reply = MOCK_RESPONSES["cosine_similarity"]
            elif "generative" in prompt.lower() or "differ" in prompt.lower():
                mock_reply = MOCK_RESPONSES["generative_ai"]
            else:
                mock_reply = "This is a demonstration response in demo mode."

            # Create mock response structure
            response_data = {
                "id": "msg_demo_123",
                "type": "message",
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": mock_reply
                    }
                ],
                "model": payload['model'],
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {
                    "input_tokens": 15,
                    "output_tokens": 120
                }
            }
            return response_data

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()

        response_data = response.json()
        return response_data

    except requests.exceptions.RequestException as e:
        print(f"✗ API Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"  Error details: {error_data}")
                # If it's an auth error, fall back to demo mode
                if "authentication" in str(error_data).lower():
                    print(f"  [Falling back to demo mode...]\n")
                    return send_llm_request(prompt, temperature, max_tokens, force_demo=True)
            except:
                print(f"  Response: {e.response.text}")
        return None

def extract_assistant_reply(response_data):
    """Extract the assistant's reply from the response."""
    try:
        if response_data and "content" in response_data:
            for block in response_data["content"]:
                if block.get("type") == "text":
                    return block.get("text", "")
        return None
    except Exception as e:
        print(f"✗ Error extracting reply: {e}")
        return None

# Query 1: Basic question
print("\n" + "=" * 70)
print("Query 1: Basic Question with Default Parameters")
print("=" * 70)

query1 = "What are the key benefits of using embeddings in machine learning?"

print(f"\nPrompt: {query1}")

response1 = send_llm_request(query1)

if response1:
    print("\n[✓] Full JSON Response (Query 1):")
    print("-" * 70)
    print(json.dumps(response1, indent=2)[:500] + "...\n[truncated for readability]\n")

    assistant_reply1 = extract_assistant_reply(response1)
    if assistant_reply1:
        print("\n[✓] Assistant Reply (Query 1):")
        print("-" * 70)
        print(assistant_reply1)

# Query 2: Different temperature and prompt
print("\n\n" + "=" * 70)
print("Query 2: Technical Question with Higher Temperature (0.9)")
print("=" * 70)

query2 = "Explain how cosine similarity works and why it's useful for comparing embeddings."

print(f"\nPrompt: {query2}")

response2 = send_llm_request(query2, temperature=0.9, max_tokens=400)

if response2:
    print("\n[✓] Full JSON Response (Query 2):")
    print("-" * 70)
    print(json.dumps(response2, indent=2)[:500] + "...\n[truncated for readability]\n")

    assistant_reply2 = extract_assistant_reply(response2)
    if assistant_reply2:
        print("\n[✓] Assistant Reply (Query 2):")
        print("-" * 70)
        print(assistant_reply2)

# Query 3: Interactive user input
print("\n\n" + "=" * 70)
print("Query 3: Dynamic User Input")
print("=" * 70)

user_input = input("\nEnter your question for the LLM (or press Enter for default): ").strip()
if not user_input:
    user_input = "What is generative AI and how does it differ from traditional machine learning?"

print(f"\nYour Question: {user_input}")

response3 = send_llm_request(user_input, temperature=0.5, max_tokens=350)

if response3:
    print("\n[✓] Full JSON Response (Query 3):")
    print("-" * 70)
    print(json.dumps(response3, indent=2)[:500] + "...\n[truncated for readability]\n")

    assistant_reply3 = extract_assistant_reply(response3)
    if assistant_reply3:
        print("\n[✓] Assistant Reply (Query 3):")
        print("-" * 70)
        print(assistant_reply3)

# Comparison summary
print("\n\n" + "=" * 70)
print("Response Comparison Summary")
print("=" * 70)

if response1 and response2:
    usage1 = response1.get("usage", {})
    usage2 = response2.get("usage", {})

    print(f"\nQuery 1 (Temp=0.7):")
    print(f"  Input tokens: {usage1.get('input_tokens', 'N/A')}")
    print(f"  Output tokens: {usage1.get('output_tokens', 'N/A')}")

    print(f"\nQuery 2 (Temp=0.9):")
    print(f"  Input tokens: {usage2.get('input_tokens', 'N/A')}")
    print(f"  Output tokens: {usage2.get('output_tokens', 'N/A')}")

    print("\nObservations:")
    print("  • Higher temperature (0.9) may produce more creative/varied responses")
    print("  • Lower temperature (0.5) produces more focused/deterministic responses")

print("\n" + "=" * 70)
print("Exercise 2 completed!")
print("=" * 70)
