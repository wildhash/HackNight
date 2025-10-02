# AI Knowledge Sprint 🚀

Fast-track hackathon project: Python 3.11 FastAPI service integrating multiple AI/ML platforms.

## 🎯 Live Demo in 60 Seconds

**Want to see it in action right now?**

```bash
docker-compose up --build
```

Then open `demo.html` in your browser for an interactive demo!

![Interactive Demo UI](https://github.com/user-attachments/assets/82044310-d084-400d-aea5-f0363e8fd324)

**Or use the quick start script:**
```bash
./start-demo.sh
```

📖 **Quick Start Guide:** [QUICKSTART.md](QUICKSTART.md)  
📖 **Full Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

## Features
- **Weaviate**: Vector database for semantic search
- **Sentence Transformers**: Text embeddings
- **Friendli.ai**: Chat/RAG capabilities
- **Comet ML**: Experiment tracking
- **Daytona**: Dev environment orchestration
- **ACI.dev**: Observability (configured via env vars)
- **Interactive Demo**: HTML interface for testing all endpoints

## Quick Start (1 Hour Setup)

### 1. Prerequisites
```bash
# Python 3.11
python3.11 --version

# Optional: Weaviate (Docker)
docker run -d -p 8080:8080 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e DEFAULT_VECTORIZER_MODULE=none \
  -e CLUSTER_HOSTNAME=node1 \
  semitechnologies/weaviate:1.22.4
```

### 2. Install Dependencies
```bash
cd ai-knowledge-sprint
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Run the Service
```bash
# With uvicorn
uvicorn main:app --reload

# Or directly
python main.py

# Or with Daytona
daytona up
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/
```

### 1. `/ingest` - Embed and Store Text
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is a modern web framework for Python",
    "metadata": "tech-docs"
  }'
```

### 2. `/search` - Semantic Search
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python web frameworks",
    "limit": 5
  }'
```

### 3. `/chat` - RAG with Friendli.ai
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is FastAPI?",
    "context_limit": 3
  }'
```

### 4. `/train` - Train Classifier with Comet
```bash
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d '{
    "X": [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0]],
    "y": [0, 0, 1, 1],
    "test_size": 0.25,
    "experiment_name": "demo-classifier"
  }'
```

## Architecture

```
┌─────────────┐
│   FastAPI   │
│   (main.py) │
└─────┬───────┘
      │
      ├─── Sentence Transformers (embeddings)
      │
      ├─── Weaviate (vector storage)
      │
      ├─── Friendli.ai (chat/RAG)
      │
      ├─── Comet ML (experiment tracking)
      │
      └─── Scikit-learn (ML training)
```

## Environment Variables

See `.env.example` for all configuration options:
- Weaviate connection
- Friendli.ai API key
- Comet ML credentials
- ACI.dev observability
- Host/port settings

## Development with Daytona

The `daytona.json` configures:
- Python 3.11 runtime
- Weaviate service (Docker)
- Auto-reload on changes
- Port forwarding (8000)

## 🌐 Deployment Options

### Local Demo (Fastest)
```bash
docker-compose up --build
# Open demo.html in your browser
```

### Cloud Deployment
- **Railway**: `railway up` (auto-detects config)
- **Render**: Connect GitHub repo, auto-deploys from `render.yaml`
- **Docker**: Use provided `Dockerfile` and `docker-compose.yml`

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🎨 Interactive Demo Interface

The project includes `demo.html` - a beautiful, interactive web interface to test all API endpoints:
- Real-time API testing
- JSON request/response viewer
- Health monitoring
- Works with any API URL (local or deployed)

Just open `demo.html` in any browser and start testing!

## Notes

- **LOC**: ~290 lines (under 300 target)
- **Setup Time**: ~45-60 minutes for full demo
- **Mock Mode**: Chat endpoint works without Friendli API key (demo mode)
- **Optional Services**: Works with/without Comet ML and ACI.dev configured

## Troubleshooting

### Weaviate Connection Error
```bash
# Check if Weaviate is running
curl http://localhost:8080/v1/.well-known/ready

# Restart Weaviate
docker restart <weaviate-container-id>
```

### Model Download Issues
```bash
# Pre-download sentence transformer model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

## License

MIT - Hackathon Ready 🎯
