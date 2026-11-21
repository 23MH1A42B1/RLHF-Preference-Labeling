import sys
import json
import subprocess
from pathlib import Path


def test_downstream_validator_valid_and_invalid(tmp_path):
    validator_path = Path(__file__).resolve().parent.parent / "downstream" / "validate_data.py"

    # Valid file
    valid_file = tmp_path / "valid.jsonl"
    valid_file.write_text(
        json.dumps({
            "prompt": "Explain photosynthesis.",
            "chosen": "Process where light energy is converted into glucose.",
            "rejected": "Process where rocks turn into plants."
        }) + "\n",
        encoding="utf-8"
    )

    p_valid = subprocess.run([sys.executable, str(validator_path), str(valid_file)], capture_output=True, text=True)
    assert p_valid.returncode == 0
    assert "Validation successful" in p_valid.stdout

    # Invalid file (missing 'rejected')
    invalid_file = tmp_path / "missing_key.jsonl"
    invalid_file.write_text(
        json.dumps({
            "prompt": "Explain photosynthesis.",
            "chosen": "Process where light energy is converted into glucose."
        }) + "\n",
        encoding="utf-8"
    )

    p_invalid = subprocess.run([sys.executable, str(validator_path), str(invalid_file)], capture_output=True, text=True)
    assert p_invalid.returncode != 0
    assert "Missing required key" in p_invalid.stderr

    # Non-existent file
    p_nonexistent = subprocess.run([sys.executable, str(validator_path), "non_existent.jsonl"], capture_output=True, text=True)
    assert p_nonexistent.returncode != 0

