import hashlib
import json
import os
from typing import List

SALT = os.getenv("SALT")


def save_info_as_json(data: List[dict], file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_jsonl(file_path: str) -> List[dict] | dict:
    with open(file_path) as f:
        data = json.load(f)
    return data


def generate_hash(identifier: str, salt: str, method: str = "sha256") -> str:
    """
    Generates a deterministic hash using the provided identifier, salt, and hash method.
    """
    salted_identifier = f"{identifier}{salt}"
    hash_function = hashlib.new(method)
    hash_function.update(salted_identifier.encode("utf-8"))
    return hash_function.hexdigest()


if __name__ == "__main__":
    email = "user@example.com"
    unique_id = generate_hash(email, SALT)
    print(f"Generated unique ID: {unique_id}")
