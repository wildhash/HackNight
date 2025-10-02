
# AI Knowledge Sprint

A minimal, runnable project that can be set up and demo'd in ~1 hour at a hackathon. This service integrates:

- **Weaviate** (vector database)
- **Comet** (experiment tracking)
- **Friendli.ai** (chat/inference)
- **Daytona** (instant cloud dev env)
- **ACI.dev** (observability hooks)

## Features

This tiny service provides:

1. **Ingest**: Embeds text and stores it in Weaviate
2. **Search**: Semantic similarity search using Weaviate
3. **Chat**: Friendli.ai-powered chat augmented with top-k search context
4. **Train**: Mock fine-tuning with sklearn logistic regression, tracked in Comet
5. **Observability**: Request/response telemetry to ACI.dev

## Quickstart

### Prerequisites

- Python 3.11+
- Weaviate instance (local or remote)

### Setup

```bash
# Clone the repository
git clone https://github.com/wildhash/HackNight.git
cd HackNight

# Set up environment
cp .env.example .env
# Edit .env and fill in your API keys and URLs

# Install dependencies
pip install -r requirements.txt
```

### Running Weaviate Locally

If you don't have a Weaviate instance, you can run one locally with Docker:

```bash
docker run -p 8080:8080 -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  semitechnologies/weaviate:latest
```

Then set `WEAVIATE_URL=http://localhost:8080` in your `.env` file.

### Start the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

The API will be available at `http://localhost:8080`

## API Endpoints

### Health Check

```bash
curl http://localhost:8080/health
```

Response:
```json
{"ok": true}
```

### Ingest Text

Embeds text and stores it in Weaviate:

```bash
curl -X POST http://localhost:8080/ingest \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello Weaviate and Comet!"}'
```

Response:
```json
{"ok": true, "id": "abc123...", "seconds": 0.123}
```

### Search

Semantic search for similar documents:

```bash
curl "http://localhost:8080/search?q=Hello&k=3"
```

Response:
```json
{
  "results": [
    {"text": "Hello Weaviate and Comet!", "score": 0.95}
  ],
  "seconds": 0.05
}
```

### Chat

Chat with Friendli.ai, augmented with search context:

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Summarize what we ingested","k":3}'
```

Response:
```json
{
  "reply": "Based on the context...",
  "context": [
    {"text": "Hello Weaviate and Comet!", "score": 0.95}
  ]
}
```

### Train

Train a simple classifier and log metrics to Comet:

```bash
curl -X POST http://localhost:8080/train \
  -H "Content-Type: application/json" \
  -d '{
    "labelled_pairs": [
      {"text":"This is positive","label":1},
      {"text":"This is negative","label":0},
      {"text":"Great product","label":1},
      {"text":"Poor quality","label":0},
      {"text":"Excellent service","label":1},
      {"text":"Terrible experience","label":0},
      {"text":"Love it","label":1},
      {"text":"Hate it","label":0},
      {"text":"Amazing","label":1},
      {"text":"Awful","label":0}
    ]
  }'
```

Response:
```json
{"ok": true, "seconds": 0.234, "accuracy": 0.85}
```

## Using Daytona

Daytona provides instant cloud development environments:

```bash
# From repository root
daytona up --file infra/daytona.json
```

This will:
1. Create a workspace with Python 3.11
2. Install all dependencies
3. Start the FastAPI application on port 8080

## Demo Script (3 minutes)

Follow these steps for a quick demo:

### 1. Ingest Sample Data

```bash
curl -X POST http://localhost:8080/ingest \
  -H "Content-Type: application/json" \
  -d '{"text":"Weaviate is a vector database that stores embeddings."}'

curl -X POST http://localhost:8080/ingest \
  -H "Content-Type: application/json" \
  -d '{"text":"Comet tracks machine learning experiments and artifacts."}'
```

### 2. Search for Content

```bash
curl "http://localhost:8080/search?q=vector%20storage&k=3"
```

This shows semantic search finding relevant documents.

### 3. Chat with Context

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What tools are we using for ML tracking?"}'
```

This demonstrates Friendli.ai responding with context from Weaviate.

### 4. Train and Track

```bash
curl -X POST http://localhost:8080/train \
  -H "Content-Type: application/json" \
  -d '{
    "labelled_pairs": [
      {"text":"This is positive","label":1},
      {"text":"This is negative","label":0},
      {"text":"Great product","label":1},
      {"text":"Poor quality","label":0},
      {"text":"Excellent service","label":1},
      {"text":"Terrible experience","label":0},
      {"text":"Love it","label":1},
      {"text":"Hate it","label":0},
      {"text":"Amazing","label":1},
      {"text":"Awful","label":0}
    ]
  }'
```

Check your Comet dashboard to see:
- Training parameters (model: logreg)
- Metrics (accuracy, train_seconds)
- Artifact (model.pkl)

### 5. Observability

Check the console for ACI.dev telemetry logs, or view events in your ACI dashboard if configured.

## Architecture

### Directory Structure

```
HackNight/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── routes/
│   │   ├── ingest.py          # Ingest endpoint
│   │   ├── search.py          # Search endpoint
│   │   ├── chat.py            # Chat endpoint
│   │   └── train.py           # Train endpoint
│   ├── services/
│   │   ├── embeddings.py      # Sentence transformer embeddings
│   │   ├── weav_client.py     # Weaviate integration
│   │   ├── friendli_client.py # Friendli.ai integration
│   │   ├── comet_tracker.py   # Comet ML tracking
│   │   └── aci_client.py      # ACI.dev telemetry
│   └── schemas/
│       ├── dto.py             # Pydantic models
│       └── models.py          # Reserved for future models
├── infra/
│   ├── daytona.json           # Daytona workspace config
│   ├── Dockerfile             # Container definition
│   └── devcontainer.json      # VS Code dev container
├── tests/
│   └── test_smoke.py          # Smoke tests
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Components

#### Embeddings
Uses `sentence-transformers/all-MiniLM-L6-v2` model (384 dimensions) for fast, quality embeddings.

#### Weaviate
Stores documents with text and vector embeddings. Uses deterministic UUIDs (SHA1 hash of text) to avoid duplicates.

#### Friendli.ai
Provides chat/inference capabilities. Falls back to placeholder text if not configured.

#### Comet ML
Tracks:
- Parameters (model names, k values)
- Metrics (latency, accuracy)
- Artifacts (trained model files)

#### ACI.dev
Sends telemetry for observability. Falls back to console logging if not configured.

## Configuration

All configuration is done via environment variables in `.env`:

```bash
# Weaviate
WEAVIATE_URL=http://localhost:8080      # Required
WEAVIATE_API_KEY=                       # Optional

# Comet
COMET_API_KEY=                          # Optional
COMET_WORKSPACE=hack                    # Optional
COMET_PROJECT=ai-knowledge-sprint       # Optional

# Friendli.ai
FRIENDLI_API_URL=https://api.friendli.ai/v1/chat/completions  # Optional
FRIENDLI_API_KEY=                       # Optional

# ACI.dev
ACI_COLLECTOR_URL=                      # Optional
ACI_API_KEY=                            # Optional
```

**Note**: Only `WEAVIATE_URL` is strictly required. Other services gracefully degrade if not configured.

## Testing

Run the smoke tests:

```bash
pytest tests/test_smoke.py -v
```

The tests verify:
- Health check endpoint
- Ingest → Search → Chat flow
- Response formats and status codes

## Docker

Build and run with Docker:

```bash
# Build
docker build -f infra/Dockerfile -t ai-knowledge-sprint .

# Run
docker run -p 8080:8080 --env-file .env ai-knowledge-sprint
```

## Development

### Hot Reload

For development with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### API Documentation

FastAPI provides automatic interactive documentation:

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## Troubleshooting

### "WEAVIATE_URL not set"

Make sure you've copied `.env.example` to `.env` and set the `WEAVIATE_URL` variable.

### Connection refused to Weaviate

Ensure Weaviate is running and accessible at the URL specified in `.env`.

### Import errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Model download slow on first run

The sentence-transformers model downloads on first use. Subsequent runs will be faster.

## License

MIT

## Contributing

Contributions welcome! This is a hackathon starter project designed to be extended and customized.
=======
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

**Quick Start:**
```bash
cd ai-knowledge-sprint
pip install -r requirements.txt
python main.py
```

**Details:** See [ai-knowledge-sprint/README.md](ai-knowledge-sprint/README.md)

**Target:** <300 LOC, runnable in 1 hour for hackathon demos
main
