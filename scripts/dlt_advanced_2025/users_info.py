import os
from typing import Any, Dict, Iterator, List

import pandas as pd
import pendulum
from dotenv import load_dotenv

import sys
sys.path.append(os.path.abspath("../"))
from legacy.utils import generate_hash

load_dotenv()
# set -a && source .env && set +a
SALT = os.getenv("SALT")


def generate_users_info(user_data: Iterator, salt: str) -> List[Dict[str, Any]]:
    df = pd.DataFrame(user_data)
    df["Timestamp"] = df["Timestamp"].apply(
        lambda x: pendulum.parse(x, strict=False).isoformat()
    )
    
    # Define passing score (70% of total possible score)
    # Adjust the total score (61) as needed for your course
    passing_threshold = 48 * 0.7
    
    # Identify those who didn't pass
    not_passed = df.loc[df["Score"] < passing_threshold, :]
    
    # Filter to only include essential columns for not_passed.csv
    essential_columns = [
        "Timestamp", 
        "Email Address", 
        "Score", 
        "Your full name. This information will be displayed on your certificate."
    ]
    
    # Only keep the columns that exist in the DataFrame
    available_columns = [col for col in essential_columns if col in not_passed.columns]
    not_passed_filtered = not_passed[available_columns]
    
    # Save the filtered DataFrame to not_passed.csv
    not_passed_filtered.to_csv("not_passed.csv", index=False)

    # Process only those who passed
    passed = df.loc[df["Score"] >= passing_threshold, :]

    # You can adjust the date filter as needed for your course
    # This filters responses after a specific date
    new = passed.loc[df["Timestamp"] > "2025-04-01T00:00:00+00:00", :]

    personal_info = []

    # Optional fields that may not exist in all forms
    github_field = "Your GitHub account username. This information will be displayed on your certificate. (Optional)"
    contact_field = "Your Contacts (e.g. link to Linkedin, email, etc.). This information will be displayed on your certificate. (Optional)"

    for i, row in new.iterrows():
        unique_user_id = generate_hash(row["Email Address"], salt)
        
        # Customize these field names to match your Google Form
        user = {
            "certificate_holder_id": unique_user_id,
            "user_name": row[
                "Your full name. This information will be displayed on your certificate."
            ],
            "passed_at": row["Timestamp"],
            "email": row["Email Address"],
            "level": 0,
            "score": row["Score"],
        }
        
        # Add optional fields only if they exist in the DataFrame
        if github_field in row.index:
            user["github"] = row[github_field]
        else:
            user["github"] = ""
            
        if contact_field in row.index:
            user["contact"] = row[contact_field]
        else:
            user["contact"] = ""
            
        personal_info.append(user)

    return personal_info 