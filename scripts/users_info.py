import os
from typing import Any, Dict, Iterator, List

import pandas as pd
import pendulum
from dotenv import load_dotenv

from utils import generate_hash

load_dotenv()
# set -a && source .env && set +a
SALT = os.getenv("SALT")


def generate_users_info(user_data: Iterator, salt: str) -> List[Dict[str, Any]]:
    df = pd.DataFrame(user_data)
    df["Timestamp"] = df["Timestamp"].apply(
        lambda x: pendulum.parse(x, strict=False).isoformat()
    )
    not_passed = df.loc[df["Score"] < 61 * 0.7, :]
    not_passed.to_csv("not_passed.csv", index=False)

    passed = df.loc[df["Score"] >= 61 * 0.7, :]

    new = passed.loc[df["Timestamp"] > "2025-03-12T17:00:00+00:00", :]

    personal_info = []

    for i, row in new.iterrows():
        unique_user_id = generate_hash(row["Email Address"], salt)
        user = {
            "certificate_holder_id": unique_user_id,
            "user_name": row[
                "Your full name. This information will be displayed on your certificate."
            ],
            "passed_at": row["Timestamp"],
            "email": row["Email Address"],
            "github": row[
                "Your GitHub account username. This information will be displayed on your certificate. (Optional)"
            ],
            "contact": row[
                "Your Contacts (e.g. link to Linkedin, email, etc.). This information will be displayed on your certificate. (Optional)\n"
            ],
            "level": 0,
            "score": row["Score"],
        }
        personal_info.append(user)

    return personal_info
