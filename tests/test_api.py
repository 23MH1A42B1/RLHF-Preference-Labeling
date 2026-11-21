import os
import sys
import json
import pytest
from pathlib import Path

# Add project root to sys.path so server module is resolved
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Use SQLite in-memory / temporary file for fast isolated automated testing
TEST_DB_URL = "sqlite:///./test_rlhf.db"
os.environ["DATABASE_URL"] = TEST_DB_URL

from server.database import Base, get_db, seed_database_if_needed, engine
from server.main import app
from server.models import Label

test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # Setup fresh tables before each test
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    # Seed data
    db = TestingSessionLocal()
    seed_file = Path(__file__).resolve().parent.parent / "data" / "seed_pairs.json"
    with open(seed_file, "r", encoding="utf-8") as f:
        seed_pairs = json.load(f)

    for p in seed_pairs:
        label = Label(
            prompt=p["prompt"],
            response_a=p["response_a"],
            response_b=p["response_b"],
            category=p["category"],
            annotator_id=None,
            chosen=None
        )
        db.add(label)
        db.flush()
        label.pair_id = label.id
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=test_engine)


def test_contract_1_database_seeding():
    """Verify that after startup/seeding, database contains at least 50 prompt-response pairs."""
    db = TestingSessionLocal()
    count = db.query(Label).count()
    db.close()
    assert count >= 50, f"Expected at least 50 pairs, found {count}"


def test_contract_2_env_example():
    """Verify that .env.example exists, contains required keys, and contains no real secrets."""
    env_file = Path(__file__).resolve().parent.parent / ".env.example"
    assert env_file.exists(), ".env.example must exist in repository root"

    content = env_file.read_text(encoding="utf-8")
    assert "DATABASE_URL" in content, ".env.example missing DATABASE_URL"
    assert "OPENAI_API_KEY" in content, ".env.example missing OPENAI_API_KEY"
    # Ensure no real secret is exposed
    assert "sk-" not in content, "Real API key should not be committed to .env.example"


def test_contract_3_database_schema():
    """Verify database schema contains table labels with all required columns."""
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()
    assert "labels" in tables, "Table 'labels' must exist in database"

    columns = {col["name"]: col for col in inspector.get_columns("labels")}
    required_cols = ["id", "prompt", "response_a", "response_b", "category", "annotator_id", "chosen"]
    for col in required_cols:
        assert col in columns, f"Column '{col}' must be present in 'labels' table"
    # Verify chosen is nullable
    assert columns["chosen"]["nullable"] is True, "Column 'chosen' must be nullable"


def test_contract_4_get_pairs_next():
    """Verify GET /api/pairs/next returns unlabeled pairs and 404 when exhausted."""
    annotator = "test_annotator_contract4"
    resp = client.get(f"/api/pairs/next?annotator_id={annotator}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    data = resp.json()

    assert "id" in data
    assert "prompt" in data
    assert "response_a" in data
    assert "response_b" in data

    # Label all pairs for this annotator
    db = TestingSessionLocal()
    all_pairs = db.query(Label).all()
    for p in all_pairs:
        # submit label
        post_resp = client.post("/api/labels", json={
            "pair_id": p.id,
            "annotator_id": annotator,
            "chosen": "A"
        })
        assert post_resp.status_code == 201
    db.close()

    # Now fetching next pair must return 404
    final_resp = client.get(f"/api/pairs/next?annotator_id={annotator}")
    assert final_resp.status_code == 404, f"Expected 404 Not Found when exhausted, got {final_resp.status_code}"


def test_contract_5_submit_label():
    """Verify POST /api/labels updates chosen column in database for specified annotator."""
    annotator = "contract5_user"
    get_resp = client.get(f"/api/pairs/next?annotator_id={annotator}")
    assert get_resp.status_code == 200
    pair_id = get_resp.json()["id"]

    post_resp = client.post("/api/labels", json={
        "pair_id": pair_id,
        "annotator_id": annotator,
        "chosen": "A"
    })
    assert post_resp.status_code == 201

    # Directly inspect database
    db = TestingSessionLocal()
    record = db.query(Label).filter(Label.id == pair_id).first()
    db.close()
    assert record is not None
    assert record.chosen == "A"
    assert record.annotator_id == annotator


def test_contract_6_and_7_export_format():
    """Verify GET /api/export produces valid JSONL with prompt, chosen, rejected."""
    # Submit at least one label
    client.post("/api/labels", json={
        "pair_id": 1,
        "annotator_id": "exporter_user",
        "chosen": "A"
    })

    resp = client.get("/api/export")
    assert resp.status_code == 200
    assert "application/x-jsonlines" in resp.headers.get("content-type", "")
    assert 'attachment; filename="labels.jsonl"' in resp.headers.get("content-disposition", "")

    # Parse JSONL content
    lines = [line.strip() for line in resp.text.strip().split("\n") if line.strip()]
    assert len(lines) >= 1

    for line in lines:
        obj = json.loads(line)
        assert "prompt" in obj and isinstance(obj["prompt"], str)
        assert "chosen" in obj and isinstance(obj["chosen"], str)
        assert "rejected" in obj and isinstance(obj["rejected"], str)


def test_contract_8_export_category_filtering():
    """Verify GET /api/export?category=... filters properly."""
    db = TestingSessionLocal()
    # Find two distinct pairs and assign categories
    p1 = db.query(Label).filter(Label.id == 1).first()
    p2 = db.query(Label).filter(Label.id == 2).first()
    p1.category = "cat_A"
    p2.category = "cat_B"
    db.commit()
    db.close()

    # Submit labels for both
    client.post("/api/labels", json={"pair_id": 1, "annotator_id": "filter_user", "chosen": "A"})
    client.post("/api/labels", json={"pair_id": 2, "annotator_id": "filter_user", "chosen": "B"})

    # Export cat_A
    resp_a = client.get("/api/export?category=cat_A")
    assert resp_a.status_code == 200
    lines_a = [json.loads(line) for line in resp_a.text.strip().split("\n") if line.strip()]
    assert len(lines_a) == 1
    assert lines_a[0]["metadata"]["category"] == "cat_A"

    # Export cat_B
    resp_b = client.get("/api/export?category=cat_B")
    assert resp_b.status_code == 200
    lines_b = [json.loads(line) for line in resp_b.text.strip().split("\n") if line.strip()]
    assert len(lines_b) == 1
    assert lines_b[0]["metadata"]["category"] == "cat_B"


def test_contract_9_analytics_distribution():
    """Verify GET /api/analytics returns accurate label distribution."""
    # Reset DB: clear chosen
    db = TestingSessionLocal()
    db.query(Label).update({Label.chosen: None, Label.annotator_id: None})
    db.commit()
    db.close()

    # Submit known set: 3 'A', 2 'B', 1 'tie'
    test_submits = [
        (1, "u1", "A"),
        (2, "u1", "A"),
        (3, "u1", "A"),
        (4, "u1", "B"),
        (5, "u1", "B"),
        (6, "u1", "tie"),
    ]
    for pid, user, choice in test_submits:
        r = client.post("/api/labels", json={"pair_id": pid, "annotator_id": user, "chosen": choice})
        assert r.status_code == 201

    resp = client.get("/api/analytics")
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_labels"] == 6
    dist = data["label_distribution"]
    assert dist["A"] == 3
    assert dist["B"] == 2
    assert dist["tie"] == 1
    assert dist["skip"] == 0


def test_contract_10_inter_rater_agreement():
    """Verify GET /api/analytics returns agreement_rate 1.0 when 3 annotators label same pair identically."""
    # Clear DB labels
    db = TestingSessionLocal()
    db.query(Label).update({Label.chosen: None, Label.annotator_id: None})
    db.commit()
    db.close()

    # Annotators 1, 2, 3 label pair 1 identically with 'A'
    for annotator in ["annotator_1", "annotator_2", "annotator_3"]:
        r = client.post("/api/labels", json={"pair_id": 1, "annotator_id": annotator, "chosen": "A"})
        assert r.status_code == 201

    resp = client.get("/api/analytics")
    assert resp.status_code == 200
    data = resp.json()

    # Check for agreement key
    assert "agreement_rate" in data or "cohens_kappa" in data or "agreement" in data
    rate = data.get("agreement_rate", data.get("agreement"))
    assert isinstance(rate, float)
    assert -1.0 <= rate <= 1.0
    assert rate == 1.0, f"Expected 1.0 for identical ratings, got {rate}"


def test_contract_11_downstream_validation_script(tmp_path):
    """Verify downstream/validate_data.py exits 0 on valid JSONL and non-zero on invalid."""
    import subprocess

    valid_file = tmp_path / "valid.jsonl"
    valid_file.write_text(
        json.dumps({"prompt": "Prompt?", "chosen": "Chosen response", "rejected": "Rejected response"}) + "\n",
        encoding="utf-8"
    )

    invalid_file = tmp_path / "invalid.jsonl"
    # Missing 'rejected' key
    invalid_file.write_text(
        json.dumps({"prompt": "Prompt?", "chosen": "Chosen response"}) + "\n",
        encoding="utf-8"
    )

    script_path = str(Path(__file__).resolve().parent.parent / "downstream" / "validate_data.py")

    # Run on valid file
    res_valid = subprocess.run([sys.executable, script_path, str(valid_file)])
    assert res_valid.returncode == 0, f"Expected returncode 0 for valid file, got {res_valid.returncode}"

    # Run on invalid file
    res_invalid = subprocess.run([sys.executable, script_path, str(invalid_file)])
    assert res_invalid.returncode != 0, f"Expected non-zero returncode for invalid file, got {res_invalid.returncode}"
