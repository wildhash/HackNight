from fastapi import APIRouter, HTTPException
from app.schemas.dto import IngestRequest
from app.services import embeddings, weav_client, comet_tracker, aci_client
import time

router = APIRouter()

@router.post("/ingest")
async def ingest(body: IngestRequest):
    t0=time.time()
    try:
        vec = embeddings.embed(body.text)
        uid = weav_client.upsert(body.text, vec)
        dt=time.time()-t0
        comet_tracker.exp().log_parameters({"embed_model":"all-MiniLM-L6-v2"})
        comet_tracker.exp().log_metric("ingest_seconds", dt)
        await aci_client.track("ingest", {"id":uid,"latency":dt})
        return {"ok": True, "id": uid, "seconds": dt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingest failed: {str(e)}")
