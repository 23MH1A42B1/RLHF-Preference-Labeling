from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from server.database import get_db
from server.models import Label
from server.schemas import LabelSubmitRequest, LabelSubmitResponse

router = APIRouter(prefix="/api", tags=["Labels"])


@router.post(
    "/labels",
    status_code=status.HTTP_201_CREATED,
    response_model=LabelSubmitResponse
)
def submit_label(
    payload: LabelSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Submit a preference label for a given prompt-response pair.
    Updates the existing record or inserts a new record for inter-rater agreement tracking.
    """
    valid_choices = ["A", "B", "tie", "skip"]
    if payload.chosen not in valid_choices:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid chosen value '{payload.chosen}'. Must be one of {valid_choices}."
        )

    # Find the primary prompt-response pair by id or pair_id
    master_pair = (
        db.query(Label)
        .filter(Label.id == payload.pair_id)
        .first()
    )

    if not master_pair:
        master_pair = (
            db.query(Label)
            .filter(Label.pair_id == payload.pair_id)
            .first()
        )

    if not master_pair:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt-response pair with ID {payload.pair_id} not found."
        )

    pair_id = master_pair.pair_id if master_pair.pair_id is not None else master_pair.id

    # Check if the master record is currently unassigned/unlabeled (chosen IS NULL)
    if master_pair.chosen is None:
        master_pair.chosen = payload.chosen
        master_pair.annotator_id = payload.annotator_id
        master_pair.labeled_at = func.now()
        if master_pair.pair_id is None:
            master_pair.pair_id = master_pair.id
        db.commit()
        db.refresh(master_pair)
    else:
        # The master pair already has a label. Check if this annotator previously labeled it.
        existing_annotator_record = (
            db.query(Label)
            .filter(
                or_(Label.pair_id == pair_id, Label.id == pair_id),
                Label.annotator_id == payload.annotator_id
            )
            .first()
        )

        if existing_annotator_record:
            # Update existing record for this annotator
            existing_annotator_record.chosen = payload.chosen
            existing_annotator_record.labeled_at = func.now()
            db.commit()
        else:
            # New annotation for the same pair from a different annotator (enables inter-rater agreement)
            new_label = Label(
                prompt=master_pair.prompt,
                response_a=master_pair.response_a,
                response_b=master_pair.response_b,
                category=master_pair.category,
                annotator_id=payload.annotator_id,
                chosen=payload.chosen,
                pair_id=pair_id,
                created_at=master_pair.created_at,
                labeled_at=func.now()
            )
            db.add(new_label)
            db.commit()

    return LabelSubmitResponse(
        status="success",
        message="Label recorded successfully",
        pair_id=payload.pair_id,
        annotator_id=payload.annotator_id,
        chosen=payload.chosen
    )

