# AI Knowledge Sprint - Deployment Guide 🚀

Quick guide to get a live demo running ASAP!

## 🎯 Quick Start Options

![Interactive Demo Interface](https://github.com/user-attachments/assets/82044310-d084-400d-aea5-f0363e8fd324)

### Option 1: Docker Compose (Recommended for Local Demo)

**Fastest way to get everything running locally:**

```bash
# 1. Clone and navigate to the project
cd ai-knowledge-sprint

# 2. Start everything with one command
docker-compose up --build
```

That's it! The API will be available at `http://localhost:8000`

**Open `demo.html` in your browser** for an interactive demo interface.

### Option 2: Quick Start Script

```bash
./start-demo.sh
```

This script will:
- Auto-detect Docker availability
- Install dependencies if needed
- Start the appropriate services
- Guide you through the setup

### Option 3: Manual Local Setup

```bash
# 1. Start Weaviate (in one terminal)
docker run -d -p 8080:8080 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e DEFAULT_VECTORIZER_MODULE=none \
  -e CLUSTER_HOSTNAME=node1 \
  semitechnologies/weaviate:1.22.4

# 2. Install dependencies and start API (in another terminal)
pip install -r requirements.txt
python main.py
```

## 🌐 Cloud Deployment Options

### Railway (Recommended for Quick Cloud Demo)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Add Weaviate service** in Railway dashboard:
   - Add new service → Docker Image
   - Image: `semitechnologies/weaviate:1.22.4`
   - Add environment variables from docker-compose.yml

4. **Configure environment variables** for your API service:
   - `WEAVIATE_URL`: Internal URL of Weaviate service
   - `PORT`: 8000
   - `HOST`: 0.0.0.0

### Render

1. **Fork this repository**

2. **Create new Web Service** on Render dashboard:
   - Connect your GitHub repository
   - Select `ai-knowledge-sprint` directory
   - Render will auto-detect the Dockerfile

3. **Set environment variables:**
   - `WEAVIATE_URL`: (use external Weaviate or skip for mock mode)
   - `FRIENDLI_API_KEY`: (optional)
   - `COMET_API_KEY`: (optional)

4. **Deploy!** Render will build and deploy automatically.

### Vercel / Netlify (Static Demo Page)

You can host just the `demo.html` page for a quick frontend demo:

1. **Point to your deployed API** by editing the API URL in demo.html
2. **Deploy demo.html** to Vercel/Netlify
3. **Share the link** for instant demo access

## 🔧 Environment Variables

### Required
- `WEAVIATE_URL`: URL of Weaviate instance (default: `http://localhost:8080`)

### Optional (Service works without these)
- `FRIENDLI_API_KEY`: For live chat/RAG (falls back to mock mode)
- `COMET_API_KEY`: For experiment tracking (optional)
- `COMET_PROJECT_NAME`: Project name for Comet
- `COMET_WORKSPACE`: Workspace name for Comet
- `ACI_API_KEY`: For observability (optional)
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)

## 📱 Using the Live Demo

### Interactive HTML Demo
1. Open `demo.html` in your browser
2. Update the API URL if needed
3. Click buttons to test each endpoint
4. See real-time responses

### API Documentation
Visit `http://your-api-url/docs` for automatic Swagger UI documentation.

### curl Examples
```bash
# Health check
curl http://localhost:8000/

# Ingest text
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"text": "FastAPI is amazing", "metadata": "demo"}'

# Search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "FastAPI", "limit": 5}'

# Chat (RAG)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is FastAPI?", "context_limit": 3}'

# Train model
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d '{
    "X": [[1,2],[2,3],[3,4],[4,5]],
    "y": [0,0,1,1],
    "test_size": 0.25
  }'
```

## 🎭 Demo Modes

### Full Mode (with Weaviate)
- All features fully functional
- Real semantic search
- Context-aware RAG

### Mock Mode (without Weaviate)
- Health check works
- Training endpoint works
- Chat returns mock responses
- Search/Ingest will fail (expected)

## 🚨 Troubleshooting

### "Connection refused" error
- Check if Weaviate is running: `curl http://localhost:8080/v1/.well-known/ready`
- Check if API is running: `curl http://localhost:8000/`

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Docker issues
```bash
# Reset Docker Compose
docker-compose down -v
docker-compose up --build
```

### Port already in use
```bash
# Change port in docker-compose.yml or .env
# Or stop conflicting service:
lsof -ti:8000 | xargs kill -9
```

## 📊 Monitoring Your Demo

### Check logs
```bash
# Docker Compose
docker-compose logs -f

# Individual container
docker logs -f ai-knowledge-sprint_api_1
```

### Health check
```bash
curl http://localhost:8000/
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

## 🎯 Quick Demo Script

For presentations or demos:

1. **Open demo.html** in your browser
2. **Click "Check Health"** - shows service is online
3. **Click "Ingest Text"** - demonstrates embedding + storage
4. **Click "Search"** - shows semantic search working
5. **Click "Chat"** - demonstrates RAG capabilities
6. **Click "Train Model"** - shows ML training with metrics

Each operation shows real-time results with formatted JSON responses.

## 📝 Notes

- **Startup time**: ~1-2 minutes for Docker Compose (model download on first run)
- **Mock mode**: Works without external dependencies for quick demos
- **Production ready**: Add authentication, rate limiting, monitoring for production use
- **Cost**: Free tier available on Railway/Render for demos

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)
