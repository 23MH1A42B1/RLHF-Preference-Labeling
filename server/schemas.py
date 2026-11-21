from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class PairResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prompt: str
    response_a: str
    response_b: str
    category: Optional[str] = None


class LabelSubmitRequest(BaseModel):
    pair_id: int
    annotator_id: str
    chosen: str = Field(..., description="Preference choice: 'A', 'B', 'tie', or 'skip'")


class LabelSubmitResponse(BaseModel):
    status: str = "success"
    message: str = "Preference label submitted successfully"
    pair_id: int
    annotator_id: str
    chosen: str


class AnalyticsResponse(BaseModel):
    total_labels: int
    label_distribution: Dict[str, int]
    agreement_rate: float
    cohens_kappa: Optional[float] = None
    multi_labeled_pairs_count: Optional[int] = 0
