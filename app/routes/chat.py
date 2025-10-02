from fastapi import APIRouter, HTTPException
from app.schemas.dto import ChatRequest, ChatResponse, SearchResponseItem
from app.services import embeddings, weav_client, friendli_client, comet_tracker, aci_client
import time

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    t0=time.time()
    try:
        qvec = embeddings.embed(body.message)
        ctx = weav_client.search(qvec, k=body.k)
        context_text = "\n\n".join([f"- {c['text']}" for c in ctx])
        messages = [
            {"role":"system","content":"You are a concise assistant. Use the provided context when helpful."},
            {"role":"user","content": f"Context:\n{context_text}\n\nUser message: {body.message}"}
        ]
        reply = await friendli_client.generate(messages)
        dt=time.time()-t0
        comet_tracker.exp().log_metric("chat_seconds", dt)
        await aci_client.track("chat", {"latency":dt})
        return ChatResponse(reply=reply, context=[SearchResponseItem(**c) for c in ctx])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
