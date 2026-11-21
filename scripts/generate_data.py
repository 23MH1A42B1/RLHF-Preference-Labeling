"""
Data Generation Script for RLHF Preference Labeling Tool
Reads seed prompts, calls an LLM API (OpenAI, Ollama, or local mock)
to generate two diverse responses per prompt, and inserts them into the database.
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/rlhf_db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai" if OPENAI_API_KEY else "mock")


def generate_with_openai(prompt: str, api_key: str, model: str = "gpt-3.5-turbo") -> Tuple[str, str]:
    """Call OpenAI API twice with different temperatures to generate diverse responses."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        # Call 1: lower temperature (more deterministic/concise)
        resp_a = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        ).choices[0].message.content.strip()

        # Call 2: higher temperature (more creative/elaborate)
        resp_b = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=300
        ).choices[0].message.content.strip()

        return resp_a, resp_b
    except Exception as e:
        print(f"OpenAI API call failed: {e}. Falling back to default responses.", file=sys.stderr)
        return generate_mock_responses(prompt)


def generate_with_ollama(prompt: str, base_url: str = "http://localhost:11434", model: str = "llama3") -> Tuple[str, str]:
    """Call local Ollama instance twice with different temperatures."""
    try:
        import urllib.request
        def call_ollama(temp: float) -> str:
            req_data = json.dumps({
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temp}
            }).encode('utf-8')
            req = urllib.request.Request(
                f"{base_url}/api/generate",
                data=req_data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as res:
                data = json.loads(res.read().decode('utf-8'))
                return data.get("response", "").strip()

        resp_a = call_ollama(0.3)
        resp_b = call_ollama(0.9)
        return resp_a, resp_b
    except Exception as e:
        print(f"Ollama call failed: {e}. Falling back to default responses.", file=sys.stderr)
        return generate_mock_responses(prompt)


def generate_mock_responses(prompt: str) -> Tuple[str, str]:
    """Fallback generator providing diverse simulated responses."""
    resp_a = f"Detailed analysis and well-structured answer addressing: '{prompt}'."
    resp_b = f"Brief and concise summary response regarding: '{prompt}'."
    return resp_a, resp_b


def insert_pairs_into_db(pairs: List[Dict], db_url: str):
    """Insert generated prompt pairs into PostgreSQL or SQLite database using SQLAlchemy."""
    from sqlalchemy import create_engine, text

    engine = create_engine(db_url)
    with engine.begin() as conn:
        # Ensure table exists
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS labels (
                id SERIAL PRIMARY KEY,
                prompt TEXT NOT NULL,
                response_a TEXT NOT NULL,
                response_b TEXT NOT NULL,
                category VARCHAR(255) NOT NULL,
                annotator_id VARCHAR(255),
                chosen VARCHAR(50),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                labeled_at TIMESTAMP WITH TIME ZONE,
                pair_id INTEGER
            );
        """))

        # Insert pairs
        count = 0
        for p in pairs:
            # Check if prompt already exists to avoid duplicates
            existing = conn.execute(
                text("SELECT id FROM labels WHERE prompt = :prompt LIMIT 1"),
                {"prompt": p["prompt"]}
            ).fetchone()

            if not existing:
                res = conn.execute(
                    text("""
                        INSERT INTO labels (prompt, response_a, response_b, category, annotator_id, chosen, created_at)
                        VALUES (:prompt, :response_a, :response_b, :category, NULL, NULL, CURRENT_TIMESTAMP)
                        RETURNING id
                    """),
                    {
                        "prompt": p["prompt"],
                        "response_a": p["response_a"],
                        "response_b": p["response_b"],
                        "category": p["category"]
                    }
                )
                new_id = res.scalar()
                # Update pair_id to match id
                conn.execute(
                    text("UPDATE labels SET pair_id = :id WHERE id = :id"),
                    {"id": new_id}
                )
                count += 1

        print(f"Successfully inserted {count} new prompt pairs into database.")


def main():
    parser = argparse.ArgumentParser(description="Generate LLM responses for seed prompts and seed the database.")
    parser.add_argument("--prompts", default="data/seed_prompts.json", help="Path to seed prompts JSON file")
    parser.add_argument("--pairs", default="data/seed_pairs.json", help="Path to pre-generated pairs JSON file (optional)")
    parser.add_argument("--use-pregenerated", action="store_true", help="Use pre-generated seed pairs directly")
    parser.add_argument("--provider", choices=["openai", "ollama", "mock"], default=LLM_PROVIDER, help="LLM Provider")
    parser.add_argument("--db-url", default=DATABASE_URL, help="Database connection URL")

    args = parser.parse_args()

    pairs = []
    if args.use_pregenerated or (not OPENAI_API_KEY and args.provider != "ollama"):
        print(f"Loading pre-generated seed pairs from {args.pairs}...")
        with open(args.pairs, "r", encoding="utf-8") as f:
            pairs = json.load(f)
    else:
        print(f"Loading seed prompts from {args.prompts}...")
        with open(args.prompts, "r", encoding="utf-8") as f:
            prompts_data = json.load(f)

        print(f"Generating 2 responses per prompt using provider '{args.provider}'...")
        for item in prompts_data:
            category = item["category"]
            prompt = item["prompt"]
            print(f"Processing: [{category}] {prompt[:40]}...")

            if args.provider == "openai" and OPENAI_API_KEY:
                resp_a, resp_b = generate_with_openai(prompt, OPENAI_API_KEY)
            elif args.provider == "ollama":
                resp_a, resp_b = generate_with_ollama(prompt, OLLAMA_BASE_URL)
            else:
                resp_a, resp_b = generate_mock_responses(prompt)

            pairs.append({
                "category": category,
                "prompt": prompt,
                "response_a": resp_a,
                "response_b": resp_b
            })

    print(f"Total pairs prepared: {len(pairs)}")
    try:
        insert_pairs_into_db(pairs, args.db_url)
    except Exception as e:
        print(f"Could not connect to DB ({args.db_url}): {e}")
        print("Note: In dockerized environments, the DB is initialized via docker-entrypoint-initdb.d/init.sql.")


if __name__ == "__main__":
    main()

