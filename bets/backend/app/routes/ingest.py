from fastapi import APIRouter
from sqlalchemy import create_engine, text
from pathlib import Path
import random, time

DB_PATH = Path(__file__).resolve().parents[2] / "db" / "data.db"
engine = create_engine(f"sqlite:///{DB_PATH}", future=True)

with engine.begin() as conn:
    conn.exec_driver_sql('''CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        t TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source TEXT,
        key TEXT,
        value REAL
    )''')

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("/run")
def run_ingest():
    # simulate 3 sources
    now = int(time.time())
    rows = []
    for src in ["spa","procon","cnc"]:
        rows += [
            {"source": src, "key": "cases", "value": random.randint(100, 1000)},
            {"source": src, "key": "amount", "value": random.uniform(10000, 400000)},
        ]
    with engine.begin() as conn:
        for r in rows:
            conn.execute(text("INSERT INTO metrics (source, key, value) VALUES (:source,:key,:value)"), r)
    return {"inserted": len(rows)}
