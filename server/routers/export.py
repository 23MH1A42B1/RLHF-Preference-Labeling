import json
from typing import Optional
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import Label

router = APIRouter(prefix="/api", tags=["Export"])


@router.get("/export")
def export_labels(
    category: Optional[str] = Query(None, description="Filter export by category"),
    db: Session = Depends(get_db)
):
    """
    Export completed preference labels in JSONL format ready for RLHF reward model training.
    Filters by category if specified.
    Transforms pairs into (prompt, chosen, rejected) format.
    """
    # Only export rows where chosen is 'A' or 'B' (omits ties and skips)
    query = db.query(Label).filter(
        Label.chosen.isnot(None),
        Label.chosen.in_(["A", "B"])
    )

    if category:
        query = query.filter(Label.category == category)

    labels = query.order_by(Label.id.asc()).all()

    lines = []
    for row in labels:
        if row.chosen == "A":
            chosen_text = row.response_a
            rejected_text = row.response_b
        elif row.chosen == "B":
            chosen_text = row.response_b
            rejected_text = row.response_a
        else:
            continue

        item = {
            "prompt": row.prompt,
            "chosen": chosen_text,
            "rejected": rejected_text,
            "metadata": {
                "category": row.category,
                "annotator_id": row.annotator_id or "unassigned",
                "label_id": row.id,
                "pair_id": row.pair_id or row.id
            }
        }
        lines.append(json.dumps(item, ensure_ascii=False))

    content = "\n".join(lines)
    if lines:
        content += "\n"

    headers = {
        "Content-Type": "application/x-jsonlines",
        "Content-Disposition": 'attachment; filename="labels.jsonl"'
    }

    return Response(
        content=content,
        media_type="application/x-jsonlines",
        headers=headers
    )

