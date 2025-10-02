#!/usr/bin/env python3
"""
Demo script showing API usage examples
Can be run without starting the full service
"""

def print_examples():
    """Print curl examples for all endpoints"""
    print("=" * 70)
    print("AI Knowledge Sprint - API Demo Examples")
    print("=" * 70)
    print()
    
    print("📋 Prerequisites:")
    print("1. Start Weaviate (optional, for full functionality):")
    print("   docker run -d -p 8080:8080 \\")
    print("     -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \\")
    print("     -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \\")
    print("     -e DEFAULT_VECTORIZER_MODULE=none \\")
    print("     -e CLUSTER_HOSTNAME=node1 \\")
    print("     semitechnologies/weaviate:1.22.4")
    print()
    print("2. Start the API server:")
    print("   python main.py")
    print()
    print("-" * 70)
    print()
    
    print("🔍 1. HEALTH CHECK")
    print("curl http://localhost:8000/")
    print()
    
    print("📥 2. INGEST TEXT")
    print("curl -X POST http://localhost:8000/ingest \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{")
    print('    "text": "FastAPI is a modern web framework for Python",')
    print('    "metadata": "tech-docs"')
    print("  }'")
    print()
    
    print("🔎 3. SEMANTIC SEARCH")
    print("curl -X POST http://localhost:8000/search \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{")
    print('    "query": "Python web frameworks",')
    print('    "limit": 5')
    print("  }'")
    print()
    
    print("💬 4. CHAT (RAG)")
    print("curl -X POST http://localhost:8000/chat \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{")
    print('    "query": "What is FastAPI?",')
    print('    "context_limit": 3')
    print("  }'")
    print()
    
    print("🤖 5. TRAIN CLASSIFIER")
    print("curl -X POST http://localhost:8000/train \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{")
    print('    "X": [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0]],')
    print('    "y": [0, 0, 1, 1],')
    print('    "test_size": 0.25,')
    print('    "experiment_name": "demo-classifier"')
    print("  }'")
    print()
    
    print("=" * 70)
    print("📚 For more details, see README.md")
    print("=" * 70)

def print_python_examples():
    """Print Python client examples"""
    print()
    print("=" * 70)
    print("Python Client Examples")
    print("=" * 70)
    print()
    
    code = '''
import httpx

BASE_URL = "http://localhost:8000"

# 1. Health check
response = httpx.get(f"{BASE_URL}/")
print(response.json())

# 2. Ingest text
response = httpx.post(
    f"{BASE_URL}/ingest",
    json={
        "text": "AI and machine learning are transforming technology",
        "metadata": "ai-docs"
    }
)
print(response.json())

# 3. Search
response = httpx.post(
    f"{BASE_URL}/search",
    json={"query": "artificial intelligence", "limit": 3}
)
print(response.json())

# 4. Chat
response = httpx.post(
    f"{BASE_URL}/chat",
    json={"query": "Tell me about AI", "context_limit": 2}
)
print(response.json())

# 5. Train
response = httpx.post(
    f"{BASE_URL}/train",
    json={
        "X": [[i, i*2] for i in range(10)],
        "y": [0]*5 + [1]*5,
        "test_size": 0.3
    }
)
print(response.json())
'''
    print(code)

if __name__ == "__main__":
    print_examples()
    print_python_examples()
