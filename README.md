# HackNight

## Projects

### ai-knowledge-sprint 🚀
FastAPI service integrating multiple AI/ML platforms for hackathon demos.

**Features:**
- Weaviate vector database for semantic search
- Sentence Transformers for text embeddings  
- Friendli.ai for chat/RAG capabilities
- Comet ML for experiment tracking
- Daytona dev environment configuration
- ACI.dev observability support
- Interactive HTML demo interface
- Docker Compose for one-command deployment
- Cloud deployment configs (Railway, Render)

**🎯 Live Demo - Quick Start:**
```bash
cd ai-knowledge-sprint
docker-compose up --build
# Then open demo.html in your browser
```

Or use the quick start script:
```bash
cd ai-knowledge-sprint
./start-demo.sh
```

**Details:** 
- Setup: [ai-knowledge-sprint/README.md](ai-knowledge-sprint/README.md)
- Deployment: [ai-knowledge-sprint/DEPLOYMENT.md](ai-knowledge-sprint/DEPLOYMENT.md)

**Target:** <300 LOC, runnable in 1 hour, deployable in minutes