from sentence_transformers import SentenceTransformer
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def embed(text: str):
    return get_model().encode([text])[0].tolist()
