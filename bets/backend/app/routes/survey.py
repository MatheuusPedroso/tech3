from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy import create_engine, text
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "db" / "data.db"
engine = create_engine(f"sqlite:///{DB_PATH}", future=True)

# init table
with engine.begin() as conn:
    conn.exec_driver_sql('''CREATE TABLE IF NOT EXISTS survey (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        t TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        age INTEGER,
        invested REAL,
        final REAL,
        game TEXT,
        rtp REAL,
        k REAL,
        spins INTEGER,
        sessions_per_month INTEGER
    )''')

class SurveyIn(BaseModel):
    age: int = Field(ge=10, le=120)
    invested: float = Field(ge=0)
    final: float = Field(ge=0)
    game: Optional[str] = None
    rtp: Optional[float] = None
    k: Optional[float] = None
    spins: Optional[int] = None
    sessions_per_month: Optional[int] = None

router = APIRouter(prefix="/survey", tags=["survey"])

@router.post("/submit")
def submit(data: SurveyIn):
    with engine.begin() as conn:
        conn.execute(text("""INSERT INTO survey (age, invested, final, game, rtp, k, spins, sessions_per_month)
            VALUES (:age, :invested, :final, :game, :rtp, :k, :spins, :sessions_per_month)"""), data.model_dump())
    return {"status":"ok"}

@router.get("/stats")
def stats():
    with engine.begin() as conn:
        row = conn.execute(text("""SELECT COUNT(*) AS n, 
                COALESCE(SUM(invested),0) AS invested,
                COALESCE(SUM(final),0) AS final
            FROM survey""")).mappings().first()
    n = row["n"]
    total_invest = float(row["invested"])
    total_final = float(row["final"])
    preju = total_invest - total_final
    avg_loss = (preju / n) if n else 0.0
    return {"n": n, "total_invested": total_invest, "total_final": total_final, "total_loss": preju, "avg_loss": avg_loss}
