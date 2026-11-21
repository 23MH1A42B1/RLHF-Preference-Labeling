from collections import Counter
from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import Label

router = APIRouter(prefix="/api", tags=["Analytics"])


@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    """
    Compute and return summary analytics for the preference labeling workflow:
    - total labels submitted
    - label distribution (counts for 'A', 'B', 'tie', 'skip')
    - inter-rater agreement rate / Cohen's Kappa
    - breakdown by category
    """
    # Query all completed labels (where chosen is NOT NULL)
    labeled_rows = (
        db.query(Label)
        .filter(Label.chosen.isnot(None))
        .all()
    )

    total_labels = len(labeled_rows)

    # Initialize distribution with all required keys
    label_distribution = {
        "A": 0,
        "B": 0,
        "tie": 0,
        "skip": 0
    }

    category_counts: Dict[str, Dict[str, int]] = {}

    for row in labeled_rows:
        choice = row.chosen.strip() if row.chosen else ""
        if choice in label_distribution:
            label_distribution[choice] += 1
        elif choice.upper() == "A":
            label_distribution["A"] += 1
        elif choice.upper() == "B":
            label_distribution["B"] += 1
        elif choice.lower() == "tie":
            label_distribution["tie"] += 1
        elif choice.lower() == "skip":
            label_distribution["skip"] += 1
        else:
            label_distribution[choice] = label_distribution.get(choice, 0) + 1

        cat = row.category or "uncategorized"
        if cat not in category_counts:
            category_counts[cat] = {"total": 0, "A": 0, "B": 0, "tie": 0, "skip": 0}
        category_counts[cat]["total"] += 1
        if choice in category_counts[cat]:
            category_counts[cat][choice] += 1

    # Inter-rater agreement computation
    # Group submitted labels by prompt-pair ID
    pair_labels: Dict[int, List[str]] = {}
    for row in labeled_rows:
        pid = row.pair_id if row.pair_id is not None else row.id
        if pid not in pair_labels:
            pair_labels[pid] = []
        pair_labels[pid].append(row.chosen)

    # Identify pairs evaluated by 2 or more distinct annotations
    multi_annotated_pairs = [labels for labels in pair_labels.values() if len(labels) > 1]

    if not multi_annotated_pairs:
        # If no pairs have multiple ratings yet, standard baseline agreement
        agreement_rate = 1.0 if total_labels > 0 else 0.0
        cohens_kappa = agreement_rate
    else:
        # Calculate average pairwise agreement for each multi-annotated pair:
        # For each pair with k annotations: sum(count_c * (count_c - 1) / 2) / (k * (k - 1) / 2)
        pair_agreements = []
        for labels in multi_annotated_pairs:
            k = len(labels)
            counts = Counter(labels)
            agreeing_pairs = sum(c * (c - 1) // 2 for c in counts.values())
            total_possible_pairs = k * (k - 1) // 2
            pair_agreements.append(agreeing_pairs / total_possible_pairs)

        avg_observed_agreement = sum(pair_agreements) / len(pair_agreements)
        agreement_rate = round(float(avg_observed_agreement), 4)

        # Expected chance agreement Pe for Cohen's Kappa approximation
        if total_labels > 0:
            pe = sum((cnt / total_labels) ** 2 for cnt in label_distribution.values() if cnt > 0)
        else:
            pe = 0.25

        if pe < 1.0 and pe >= 0:
            kappa = (avg_observed_agreement - pe) / (1.0 - pe)
            cohens_kappa = round(float(max(-1.0, min(1.0, kappa))), 4)
        else:
            cohens_kappa = agreement_rate

    return {
        "total_labels": total_labels,
        "label_distribution": label_distribution,
        "agreement_rate": agreement_rate,
        "agreement": agreement_rate,
        "cohens_kappa": cohens_kappa,
        "multi_labeled_pairs_count": len(multi_annotated_pairs),
        "category_breakdown": category_counts
    }

