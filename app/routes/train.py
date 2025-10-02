from fastapi import APIRouter
from app.schemas.dto import TrainRequest
from app.services import embeddings, comet_tracker, aci_client
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np, pickle, time, asyncio

router = APIRouter()

@router.post("/train")
async def train(body: TrainRequest):
    if not body.labelled_pairs:
        return {"ok": False, "msg": "Provide labelled_pairs [{text,label}]."}
    X = np.vstack([embeddings.embed(p.text) for p in body.labelled_pairs])
    y = np.array([p.label for p in body.labelled_pairs])
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)
    t0=time.time()
    clf = LogisticRegression(max_iter=200).fit(Xtr, ytr)
    dt=time.time()-t0
    acc = float(accuracy_score(yte, clf.predict(Xte)))
    comet_tracker.exp().log_parameters({"model":"logreg"})
    comet_tracker.exp().log_metric("train_seconds", dt)
    comet_tracker.exp().log_metric("accuracy", acc)
    with open("model.pkl","wb") as f: pickle.dump(clf, f)
    try: comet_tracker.exp().log_asset("model.pkl")
    except: pass
    await aci_client.track("train", {"latency":dt,"accuracy":acc})
    return {"ok": True, "seconds": dt, "accuracy": acc}
