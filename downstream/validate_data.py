#!/usr/bin/env python3
"""
Downstream Validation Script for RLHF Dataset.
Simulates a downstream consumer / training pipeline validator that reads exported JSONL data,
verifies JSON validity on every line, and checks that required keys ('prompt', 'chosen', 'rejected')
are present and are non-empty strings.
"""

import sys
import os
import json


def validate_file(filepath: str) -> bool:
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' does not exist.", file=sys.stderr)
        return False

    line_count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            line_count += 1
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Validation Error [line {line_num}]: Invalid JSON - {e}", file=sys.stderr)
                return False

            if not isinstance(data, dict):
                print(f"Validation Error [line {line_num}]: Expected a JSON object, got {type(data).__name__}", file=sys.stderr)
                return False

            for required_key in ["prompt", "chosen", "rejected"]:
                if required_key not in data:
                    print(f"Validation Error [line {line_num}]: Missing required key '{required_key}'", file=sys.stderr)
                    return False
                if not isinstance(data[required_key], str):
                    print(f"Validation Error [line {line_num}]: Value for '{required_key}' must be a string", file=sys.stderr)
                    return False

    if line_count == 0:
        print("Validation Notice: File is empty or contains only whitespace.", file=sys.stderr)

    print(f"Validation successful! Processed {line_count} valid records.")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python downstream/validate_data.py <path_to_labels.jsonl>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    is_valid = validate_file(filepath)

    if is_valid:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

