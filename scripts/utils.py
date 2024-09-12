import json
from typing import List


def save_info_as_json(data: List[dict], file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_jsonl(file_path: str) -> List[dict] | dict:
    with open(file_path) as f:
        data = json.load(f)
    return data
