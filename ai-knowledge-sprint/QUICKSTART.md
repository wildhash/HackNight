# 🚀 Quick Start - Live Demo in 60 Seconds

Get a live demo running ASAP with just one command!

## The Fastest Way

```bash
cd ai-knowledge-sprint
docker-compose up --build
```

**That's it!** In about 2 minutes you'll have:
- ✅ Weaviate vector database running
- ✅ FastAPI service with all endpoints
- ✅ Automatic model download
- ✅ Full functionality ready to demo

## Open the Interactive Demo

Open `demo.html` in your browser for a beautiful interface:

![Demo Interface](https://github.com/user-attachments/assets/82044310-d084-400d-aea5-f0363e8fd324)

### What You Get

🔍 **Health Check** - Verify service is running
📥 **Ingest Text** - Add documents with embeddings
🔎 **Semantic Search** - Find similar documents
💬 **Chat (RAG)** - AI-powered Q&A with context
🤖 **Train Classifier** - ML training with metrics

## Alternative: Quick Start Script

```bash
./start-demo.sh
```

This smart script will:
- Detect if Docker is available
- Auto-install dependencies if needed
- Start the appropriate services
- Guide you through setup

## No Docker? No Problem!

### Option 1: API Only (Mock Mode)
```bash
pip install -r requirements.txt
python main.py
```

Some features will work in mock mode without Weaviate.

### Option 2: Manual Setup
```bash
# Terminal 1: Start Weaviate
docker run -d -p 8080:8080 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e DEFAULT_VECTORIZER_MODULE=none \
  -e CLUSTER_HOSTNAME=node1 \
  semitechnologies/weaviate:1.22.4

# Terminal 2: Start API
pip install -r requirements.txt
python main.py
```

## Test the API

### With the Interactive UI
1. Open `demo.html` in any browser
2. Click any button to test endpoints
3. See real-time JSON responses

### With curl
```bash
# Health check
curl http://localhost:8000/

# Ingest some data
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"text": "FastAPI is amazing", "metadata": "demo"}'

# Search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "FastAPI", "limit": 5}'
```

### With Python
```python
import httpx

# Test health
response = httpx.get("http://localhost:8000/")
print(response.json())

# Ingest data
response = httpx.post(
    "http://localhost:8000/ingest",
    json={"text": "AI is transforming technology", "metadata": "ai-docs"}
)
print(response.json())
```

## Deploy to Cloud (2 Minutes)

### Railway
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Render
1. Fork the repository
2. Connect to Render
3. Deploy automatically

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed cloud deployment instructions.

## What's Running?

When you use `docker-compose up`:
- **Port 8000**: FastAPI service (API endpoints)
- **Port 8080**: Weaviate vector database
- **Port 9000**: (optional) HTTP server for demo.html

## Troubleshooting

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in .env
echo "PORT=8001" >> .env
```

### Docker issues
```bash
# Reset everything
docker-compose down -v
docker-compose up --build
```

### Dependencies missing
```bash
pip install -r requirements.txt
```

## Next Steps

- 📖 Read [README.md](README.md) for detailed API documentation
- 🌐 Check [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment
- 🔧 Review [OVERVIEW.md](OVERVIEW.md) for technical details
- 🧪 Run `python test_api.py` for automated tests
- 📚 View API docs at `http://localhost:8000/docs`

## Live Demo Checklist

For presentations or demos, follow this sequence:

1. ✅ Start services: `docker-compose up`
2. ✅ Open `demo.html` in browser
3. ✅ Click "Check Health" (shows service is online)
4. ✅ Click "Ingest Text" (demonstrates embedding + storage)
5. ✅ Click "Search" (shows semantic search)
6. ✅ Click "Chat" (demonstrates RAG)
7. ✅ Click "Train Model" (shows ML training)

Each step shows real-time JSON responses with actual data!

## Why This Works

- **Zero configuration**: Everything works out of the box
- **Mock mode support**: Works even without all services
- **Fast startup**: ~2 minutes to fully operational
- **Production-ready**: Same setup scales to production
- **Visual feedback**: Beautiful UI shows exactly what's happening

---

**Time to demo: 60 seconds** ⚡️
