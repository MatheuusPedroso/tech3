from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import survey, ml, ingest, metrics

app = FastAPI(title="Probabilidade Bets API", version="1.0.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "ok": True,
        "name": "Probabilidade Bets API",
        "routes": ["/api/survey/*", "/ml/*", "/ingest/run", "/metrics/latest", "/metrics/history/{source}"]
    }

# include routers (avoid duplicating prefix)
app.include_router(survey.router, prefix="/api")
app.include_router(ml.router, prefix="/ml")
app.include_router(ingest.router)   # already has /ingest
app.include_router(metrics.router)  # already has /metrics
