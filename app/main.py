import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import ingest, search, chat, train
from app.services import weav_client

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure Weaviate schema exists
    try:
        weav_client.ensure_schema()
    except Exception as e:
        print(f"Warning: Could not initialize Weaviate schema: {e}")
        print("The app will continue, but /ingest and /search may fail without Weaviate")
    yield
    # Shutdown: cleanup if needed

app = FastAPI(title="AI Knowledge Sprint", version="0.1.0", lifespan=lifespan)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(ingest.router, prefix="")
app.include_router(search.router, prefix="")
app.include_router(chat.router, prefix="")
app.include_router(train.router, prefix="")
