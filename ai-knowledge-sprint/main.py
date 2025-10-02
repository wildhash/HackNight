"""
AI Knowledge Sprint - FastAPI service with Weaviate, Comet, and Friendli.ai
Target: <300 LOC, hackathon-ready in 1 hour
"""
import os
from typing import List, Optional
from contextlib import asynccontextmanager
import httpx
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import weaviate

# Load environment variables
load_dotenv()

# Global variables
model = None
weaviate_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources"""
    global model, weaviate_client
    
    # Initialize sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize Weaviate client
    weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    weaviate_client = weaviate.Client(url=weaviate_url)
    
    # Create schema if it doesn't exist
    try:
        weaviate_client.schema.get("Document")
    except:
        schema = {
            "class": "Document",
            "properties": [
                {"name": "text", "dataType": ["text"]},
                {"name": "metadata", "dataType": ["text"]},
            ],
            "vectorizer": "none"
        }
        weaviate_client.schema.create_class(schema)
    
    yield
    
    # Cleanup
    model = None
    weaviate_client = None

app = FastAPI(
    title="AI Knowledge Sprint",
    description="FastAPI service with Weaviate, Comet, and Friendli.ai integrations",
    version="1.0.0",
    lifespan=lifespan
)

# Pydantic models
class IngestRequest(BaseModel):
    text: str
    metadata: Optional[str] = ""

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

class ChatRequest(BaseModel):
    query: str
    context_limit: int = 3

class TrainRequest(BaseModel):
    X: List[List[float]]
    y: List[int]
    test_size: float = 0.2
    experiment_name: Optional[str] = "sklearn-classifier"

# Routes
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "ai-knowledge-sprint",
        "endpoints": ["/ingest", "/search", "/chat", "/train"]
    }

@app.post("/ingest")
async def ingest(request: IngestRequest):
    """Embed text with sentence-transformers and store in Weaviate"""
    try:
        # Generate embedding
        embedding = model.encode(request.text).tolist()
        
        # Store in Weaviate
        data_object = {
            "text": request.text,
            "metadata": request.metadata
        }
        
        result = weaviate_client.data_object.create(
            data_object=data_object,
            class_name="Document",
            vector=embedding
        )
        
        return {
            "status": "success",
            "id": result,
            "text_length": len(request.text),
            "embedding_dim": len(embedding)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/search")
async def search(request: SearchRequest):
    """Semantic search using Weaviate"""
    try:
        # Generate query embedding
        query_embedding = model.encode(request.query).tolist()
        
        # Search in Weaviate
        results = weaviate_client.query.get(
            "Document", 
            ["text", "metadata"]
        ).with_near_vector({
            "vector": query_embedding
        }).with_limit(request.limit).do()
        
        documents = results.get("data", {}).get("Get", {}).get("Document", [])
        
        return {
            "status": "success",
            "query": request.query,
            "results": documents,
            "count": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/chat")
async def chat(request: ChatRequest):
    """RAG with Friendli.ai - retrieve context and generate response"""
    try:
        # Step 1: Retrieve relevant context
        query_embedding = model.encode(request.query).tolist()
        
        results = weaviate_client.query.get(
            "Document",
            ["text"]
        ).with_near_vector({
            "vector": query_embedding
        }).with_limit(request.context_limit).do()
        
        documents = results.get("data", {}).get("Get", {}).get("Document", [])
        context = "\n".join([doc.get("text", "") for doc in documents])
        
        # Step 2: Generate response with Friendli.ai
        friendli_api_key = os.getenv("FRIENDLI_API_KEY")
        friendli_url = os.getenv("FRIENDLI_API_URL", "https://api.friendli.ai/v1")
        
        if not friendli_api_key:
            # Return mock response if API key not configured
            return {
                "status": "success",
                "query": request.query,
                "context_used": len(documents),
                "response": f"[Mock Response - Configure FRIENDLI_API_KEY]\nBased on {len(documents)} documents: {context[:200]}...",
                "mode": "mock"
            }
        
        # Make request to Friendli.ai
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{friendli_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {friendli_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama-3-8b-instruct",
                    "messages": [
                        {"role": "system", "content": f"Answer based on this context:\n{context}"},
                        {"role": "user", "content": request.query}
                    ],
                    "max_tokens": 500
                }
            )
            response.raise_for_status()
            result = response.json()
        
        return {
            "status": "success",
            "query": request.query,
            "context_used": len(documents),
            "response": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
            "mode": "live"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.post("/train")
async def train(request: TrainRequest):
    """Train sklearn classifier with Comet ML logging"""
    try:
        # Initialize Comet
        comet_api_key = os.getenv("COMET_API_KEY")
        comet_project = os.getenv("COMET_PROJECT_NAME", "ai-knowledge-sprint")
        comet_workspace = os.getenv("COMET_WORKSPACE")
        
        experiment = None
        if comet_api_key:
            try:
                import comet_ml
                experiment = comet_ml.Experiment(
                    api_key=comet_api_key,
                    project_name=comet_project,
                    workspace=comet_workspace
                )
                experiment.set_name(request.experiment_name)
            except:
                pass  # Continue without Comet if initialization fails
        
        # Prepare data
        X = np.array(request.X)
        y = np.array(request.y)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=request.test_size, random_state=42
        )
        
        # Train classifier
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        
        # Evaluate
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # Log to Comet
        if experiment:
            experiment.log_parameters({
                "n_estimators": 100,
                "test_size": request.test_size,
                "n_samples": len(X),
                "n_features": X.shape[1]
            })
            experiment.log_metrics({
                "accuracy": accuracy,
                "precision": report.get("weighted avg", {}).get("precision", 0),
                "recall": report.get("weighted avg", {}).get("recall", 0),
                "f1_score": report.get("weighted avg", {}).get("f1-score", 0)
            })
            experiment.end()
        
        return {
            "status": "success",
            "accuracy": float(accuracy),
            "metrics": {
                "precision": report.get("weighted avg", {}).get("precision", 0),
                "recall": report.get("weighted avg", {}).get("recall", 0),
                "f1_score": report.get("weighted avg", {}).get("f1-score", 0)
            },
            "experiment_name": request.experiment_name,
            "comet_logged": experiment is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000))
    )
