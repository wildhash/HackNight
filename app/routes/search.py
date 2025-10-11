from fastapi import APIRouter, Query, HTTPException
from app.services import embeddings, weav_client, comet_tracker, aci_client
import time

router = APIRouter()

@router.get("/search")
async def search(q: str = Query(...), k: int = 5):
    t0=time.time()
    try:
        vec = embeddings.embed(q)
        hits = weav_client.search(vec, k=k)
        dt=time.time()-t0
        comet_tracker.exp().log_metric("search_seconds", dt)
        await aci_client.track("search", {"q":q,"k":k,"latency":dt,"hits":len(hits)})
        return {"results": hits, "seconds": dt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
