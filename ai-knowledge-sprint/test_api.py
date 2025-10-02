"""
Simple test script for AI Knowledge Sprint API
Run with: python test_api.py
"""
import httpx
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    response = httpx.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✓ Health check passed\n")

def test_ingest():
    """Test ingest endpoint"""
    print("Testing ingest...")
    data = {
        "text": "FastAPI is a modern, fast web framework for building APIs with Python",
        "metadata": "tech-docs"
    }
    response = httpx.post(f"{BASE_URL}/ingest", json=data, timeout=30.0)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✓ Ingest passed\n")

def test_search():
    """Test search endpoint"""
    print("Testing search...")
    data = {
        "query": "Python web framework",
        "limit": 3
    }
    response = httpx.post(f"{BASE_URL}/search", json=data, timeout=30.0)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✓ Search passed\n")

def test_chat():
    """Test chat endpoint"""
    print("Testing chat...")
    data = {
        "query": "What is FastAPI?",
        "context_limit": 2
    }
    response = httpx.post(f"{BASE_URL}/chat", json=data, timeout=30.0)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✓ Chat passed\n")

def test_train():
    """Test train endpoint"""
    print("Testing train...")
    data = {
        "X": [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0], 
              [5.0, 6.0], [6.0, 7.0], [7.0, 8.0], [8.0, 9.0]],
        "y": [0, 0, 0, 0, 1, 1, 1, 1],
        "test_size": 0.25,
        "experiment_name": "test-classifier"
    }
    response = httpx.post(f"{BASE_URL}/train", json=data, timeout=30.0)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✓ Train passed\n")

if __name__ == "__main__":
    print("=" * 50)
    print("AI Knowledge Sprint API Tests")
    print("=" * 50 + "\n")
    
    try:
        test_health()
        time.sleep(1)
        
        test_ingest()
        time.sleep(1)
        
        test_search()
        time.sleep(1)
        
        test_chat()
        time.sleep(1)
        
        test_train()
        
        print("=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        print("\nMake sure:")
        print("1. Server is running: python main.py")
        print("2. Weaviate is running on port 8080")
        print("3. Dependencies are installed: pip install -r requirements.txt")
