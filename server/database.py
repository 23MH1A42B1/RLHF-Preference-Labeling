import os
import json
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/rlhf_db")

# Support SQLite fallback if testing locally without Postgres
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_database_if_needed():
    """Ensure database is seeded with initial prompt-response pairs if < 50 items exist."""
    from server.models import Label

    # Create tables if not present
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        count = db.query(Label).count()
        if count < 50:
            print(f"Database currently has {count} records. Seeding initial pairs...")
            seed_file = Path(__file__).resolve().parent.parent / "data" / "seed_pairs.json"
            if seed_file.exists():
                with open(seed_file, "r", encoding="utf-8") as f:
                    seed_pairs = json.load(f)

                inserted = 0
                for idx, p in enumerate(seed_pairs, start=1):
                    # Check if prompt already exists
                    exists = db.query(Label).filter(Label.prompt == p["prompt"]).first()
                    if not exists:
                        new_label = Label(
                            prompt=p["prompt"],
                            response_a=p["response_a"],
                            response_b=p["response_b"],
                            category=p["category"],
                            annotator_id=None,
                            chosen=None,
                            pair_id=None
                        )
                        db.add(new_label)
                        db.flush()
                        new_label.pair_id = new_label.id
                        inserted += 1
                db.commit()
                print(f"Successfully seeded {inserted} prompt-response pairs.")
            else:
                print(f"Seed file not found at {seed_file}.")
        else:
            print(f"Database already contains {count} prompt-response pairs.")
    except Exception as e:
        print(f"Warning during seed check: {e}")
        db.rollback()
    finally:
        db.close()

