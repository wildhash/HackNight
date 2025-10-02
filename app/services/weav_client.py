import os, weaviate
from weaviate.classes.config import Property, DataType
from weaviate.classes.init import Auth

WEAV_CLASS = "Document"

def client():
    url = os.getenv("WEAVIATE_URL")
    api_key = os.getenv("WEAVIATE_API_KEY")
    if not url:
        raise RuntimeError("WEAVIATE_URL not set")
    auth = Auth.api_key(api_key) if api_key else None
    return weaviate.WeaviateClient(url=url, auth_client_secret=auth)

def ensure_schema(dim=384):
    c = client()
    schema = c.collections
    if WEAV_CLASS not in [col.name for col in schema.list_all()]:
        schema.create(
            name=WEAV_CLASS,
            properties=[
                Property(name="text", data_type=DataType.TEXT)
            ],
            vectorizer_config={"vectorizer": "none", "dimensions": dim},
        )

def upsert(text: str, embedding):
    import hashlib, json
    ensure_schema(dim=len(embedding))
    c = client().collections.get(WEAV_CLASS)
    uid = hashlib.sha1(text.encode("utf-8")).hexdigest()
    c.data.insert(uuid=uid, properties={"text": text}, vector=embedding)
    return uid

def search(query_embedding, k=5):
    c = client().collections.get(WEAV_CLASS)
    res = c.query.near_vector(query_embedding, limit=k, return_metadata=["distance"])
    out=[]
    for o in res.objects:
        out.append({"text": o.properties.get("text",""), "score": 1.0 - float(o.metadata.get("distance",0.0))})
    return out
