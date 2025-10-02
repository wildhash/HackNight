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

**🎯 Live Demo - Quick Start (60 seconds):**
```bash
cd ai-knowledge-sprint
docker-compose up --build
# Then open demo.html in your browser
```

![Interactive Demo](https://github.com/user-attachments/assets/82044310-d084-400d-aea5-f0363e8fd324)

Or use the quick start script:
```bash
cd ai-knowledge-sprint
./start-demo.sh
```

**Documentation:** 
- Quick Start: [ai-knowledge-sprint/QUICKSTART.md](ai-knowledge-sprint/QUICKSTART.md)
- Full Setup: [ai-knowledge-sprint/README.md](ai-knowledge-sprint/README.md)
- Deployment: [ai-knowledge-sprint/DEPLOYMENT.md](ai-knowledge-sprint/DEPLOYMENT.md)

**Target:** <300 LOC, runnable in 1 hour, deployable in minutes