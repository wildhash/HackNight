import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import ingest, search, chat, train
from app.services import weav_client

load_dotenv()

app = FastAPI(title="AI Knowledge Sprint", version="0.1.0")

@app.on_event("startup")
def _startup():
    weav_client.ensure_schema()

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(ingest.router, prefix="")
app.include_router(search.router, prefix="")
app.include_router(chat.router, prefix="")
app.include_router(train.router, prefix="")
