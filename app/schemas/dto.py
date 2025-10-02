from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    text: str

class SearchResponseItem(BaseModel):
    text: str
    score: float

class ChatRequest(BaseModel):
    message: str
    k: int = 3

class ChatResponse(BaseModel):
    reply: str
    context: List[SearchResponseItem]

class TrainExample(BaseModel):
    text: str
    label: int

class TrainRequest(BaseModel):
    labelled_pairs: List[TrainExample] = []
