from fastapi import APIRouter, Query
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

router = APIRouter(tags=["ml"])

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "text_model.pkl"

def build_dataset():
    pos = [
        "perdi dinheiro no cassino online",
        "estou endividado por causa de apostas",
        "aposta me fez perder salário",
        "não consigo parar de apostar e só perco",
        "cassino levou minhas economias",
    ]
    neg = [
        "mercado financeiro subiu hoje",
        "joguei futebol com amigos",
        "estou estudando programação",
        "economia apresentou crescimento",
        "fiz caminhada no parque",
    ]
    X = pos + neg
    y = [1]*len(pos) + [0]*len(neg)
    return X, y

@router.post("/train")
def train():
    X, y = build_dataset()
    pipe = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression(max_iter=200))])
    pipe.fit(X, y)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    return {"status":"ok", "saved": str(MODEL_PATH), "n_docs": len(X)}

@router.post("/predict")
def predict(text: str = Query(..., description="texto para classificar")):
    if not MODEL_PATH.exists():
        train()
    pipe = joblib.load(MODEL_PATH)
    proba = float(pipe.predict_proba([text])[0][1])
    label = "risco/perda" if proba >= 0.5 else "neutro"
    return {"label": label, "proba": proba}
