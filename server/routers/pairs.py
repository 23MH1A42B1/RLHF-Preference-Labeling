from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from server.database import get_db
from server.models import Label
from server.schemas import PairResponse

router = APIRouter(prefix="/api", tags=["Pairs"])


@router.get("/pairs/next", response_model=PairResponse)
def get_next_pair(
    annotator_id: str = Query(..., description="Unique identifier for the annotator"),
    category: Optional[str] = Query(None, description="Optional category filter"),
    db: Session = Depends(get_db)
):
    """
    Fetch the next available prompt-response pair that the specified annotator_id has not yet labeled.
    Returns 404 if all pairs have been labeled by this annotator.
    """
    # Subquery: get all pair IDs that this annotator has already labeled (chosen is NOT NULL)
    labeled_subquery = (
        db.query(func.coalesce(Label.pair_id, Label.id))
        .filter(
            Label.annotator_id == annotator_id,
            Label.chosen.isnot(None)
        )
        .distinct()
        .scalar_subquery()
    )

    # Master query: find seed / original pairs not in the subquery
    query = (
        db.query(Label)
        .filter(
            or_(Label.pair_id == Label.id, Label.pair_id.is_(None)),
            Label.id.notin_(labeled_subquery)
        )
    )

    if category:
        query = query.filter(Label.category == category)

    pair = query.order_by(Label.id.asc()).first()

    if not pair:
        raise HTTPException(
            status_code=404,
            detail="No unlabeled pairs available for this annotator."
        )

    return PairResponse(
        id=pair.id,
        prompt=pair.prompt,
        response_a=pair.response_a,
        response_b=pair.response_b,
        category=pair.category
    )


@router.get("/pairs/progress")
def get_annotator_progress(
    annotator_id: str = Query(..., description="Annotator ID to check progress for"),
    db: Session = Depends(get_db)
):
    """Return progress metrics for the given annotator."""
    # Count distinct total pairs in system
    total_pairs = (
        db.query(func.count(Label.id))
        .filter(or_(Label.pair_id == Label.id, Label.pair_id.is_(None)))
        .scalar() or 0
    )

    # Count distinct pairs labeled by this annotator
    labeled_count = (
        db.query(func.count(func.distinct(func.coalesce(Label.pair_id, Label.id))))
        .filter(
            Label.annotator_id == annotator_id,
            Label.chosen.isnot(None)
        )
        .scalar() or 0
    )

    return {
        "annotator_id": annotator_id,
        "total_pairs": total_pairs,
        "labeled_pairs": labeled_count,
        "remaining_pairs": max(0, total_pairs - labeled_count),
        "completion_percentage": round((labeled_count / total_pairs * 100), 1) if total_pairs > 0 else 0
    }
