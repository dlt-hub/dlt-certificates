import hashlib
import os

SALT = os.getenv("SALT")


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
