#!/usr/bin/env python3
"""
Exercise 2: Calling LLM via API
Send queries to LLM endpoint, parse responses, and compare different parameters.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('ANTHROPIC_API_KEY')

if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

# API Configuration
API_URL = "https://llmgw-wp.tekstac.com/v1/chat/completions"
HEADERS = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

def send_llm_request(prompt, temperature=0.7, max_tokens=300):
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
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Details: {e.response.text}")
        return None

def extract_assistant_reply(response_data):
    """Extract the assistant's reply from the response."""
    try:
        if response_data and "choices" in response_data:
            return response_data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        pass
    return None

# Query 1: First question with temperature=0.7
print("=" * 70)
print("Query 1: What are the benefits of embeddings in machine learning?")
print("=" * 70)

query1 = "What are the key benefits of using embeddings in machine learning?"
response1 = send_llm_request(query1, temperature=0.7)

if response1:
    print("\nFull JSON Response:")
    print(json.dumps(response1, indent=2)[:500] + "...\n")

    assistant_reply = extract_assistant_reply(response1)
    print("\nAssistant Reply:")
    print("-" * 70)
    print(assistant_reply)
    print("-" * 70)

# Query 2: Second question with different temperature for comparison
print("\n\n" + "=" * 70)
print("Query 2: Explain cosine similarity (temperature=0.9)")
print("=" * 70)

query2 = "Explain how cosine similarity works and why it's useful for comparing embeddings."
response2 = send_llm_request(query2, temperature=0.9)

if response2:
    print("\nFull JSON Response:")
    print(json.dumps(response2, indent=2)[:500] + "...\n")

    assistant_reply = extract_assistant_reply(response2)
    print("\nAssistant Reply:")
    print("-" * 70)
    print(assistant_reply)
    print("-" * 70)

# Query 3: Accept dynamic user input
print("\n\n" + "=" * 70)
print("Query 3: Your Custom Question")
print("=" * 70)

user_prompt = input("\nEnter your question: ")
response3 = send_llm_request(user_prompt, temperature=0.5)

if response3:
    print("\nFull JSON Response:")
    print(json.dumps(response3, indent=2)[:500] + "...\n")

    assistant_reply = extract_assistant_reply(response3)
    print("\nAssistant Reply:")
    print("-" * 70)
    print(assistant_reply)
    print("-" * 70)
