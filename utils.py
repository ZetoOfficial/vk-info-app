import json
from typing import Any, Dict


def save_to_json(data: Dict[str, Any], filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
