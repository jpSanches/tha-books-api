from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.deps import get_db
from datetime import datetime, timezone

router = APIRouter(tags=["Health"])


@router.get("/healthz")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "db": "reachable",
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            "version": "1.0.0",
        }
    except Exception as e:
        return {"status": "error", "db": "unreachable", "error": str(e)}
