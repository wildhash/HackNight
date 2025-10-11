import os, httpx, asyncio, json

URL=os.getenv("ACI_COLLECTOR_URL")
KEY=os.getenv("ACI_API_KEY")

async def track(event: str, payload: dict):
    data={"event":event,"payload":payload}
    if not URL or not KEY:
        print("[ACI]", json.dumps(data))
        return
    try:
        async with httpx.AsyncClient(timeout=3.0) as cx:
            await cx.post(URL, json=data, headers={"Authorization": f"Bearer {KEY}"})
    except Exception as _:
        pass
