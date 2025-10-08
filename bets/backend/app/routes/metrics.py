from fastapi import APIRouter
from sqlalchemy import create_engine, text
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "db" / "data.db"
engine = create_engine(f"sqlite:///{DB_PATH}", future=True)

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/latest")
def latest():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT t, source, key, value
            FROM metrics
            WHERE id IN (
                SELECT MAX(id) FROM metrics GROUP BY source, key
            )
        """)).mappings().all()
    return [dict(r) for r in rows]

@router.get("/history/{source}")
def history(source: str):
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT t, key, value FROM metrics
            WHERE source=:s
            ORDER BY id ASC
        """), {"s": source}).mappings().all()
    return [dict(r) for r in rows]
