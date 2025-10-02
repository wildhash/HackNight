import os, httpx

API_URL = os.getenv("FRIENDLI_API_URL")
API_KEY = os.getenv("FRIENDLI_API_KEY")

async def generate(messages):
    if not API_URL or not API_KEY:
        return "Friendli not configured; returning local placeholder."
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type":"application/json"}
    payload = {"model":"friendli-quick","messages":messages}
    try:
        async with httpx.AsyncClient(timeout=5.0) as cx:
            r = await cx.post(API_URL, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            return data.get("choices",[{}])[0].get("message",{}).get("content","(no content)")
    except Exception as e:
        return f"(Friendli error: {e})"
