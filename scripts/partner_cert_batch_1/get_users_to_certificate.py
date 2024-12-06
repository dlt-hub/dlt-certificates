import argparse
import os
import sys
from typing import Any, Iterator, List

import pandas as pd
import pendulum
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

sys.path.append(os.path.abspath("../"))
from scripts.utils import generate_hash, save_info_as_json

load_dotenv()
# set -a && source .env && set +a
SHEET_ID = os.getenv("SHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
CREDENTIALS_INFO = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
SALT = os.getenv("SALT")


def _initialize_sheets(credentials: Any) -> Any:
    # Build the service object.
    service = build("sheets", "v4", credentials=credentials)
    return service


def get_sheet(credentials: Any, spreadsheet_id: str, sheet_name: str) -> Iterator:
    sheets = _initialize_sheets(credentials)
    result = (
        sheets.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=sheet_name,
            # unformatted returns typed values
            valueRenderOption="UNFORMATTED_VALUE",
            # will return formatted dates
            dateTimeRenderOption="FORMATTED_STRING",
        )
        .execute()
    )

    values = result.get("values")

    # yield dicts assuming row 0 contains headers and following rows values and all rows have identical length
    for v in values[1:]:
        yield dict(zip(values[0], v))


def get_credentials(credentials_info: str | dict) -> Any:
    if credentials_info.endswith("json"):
        credentials = Credentials.from_service_account_file(credentials_info)
    else:
        credentials = Credentials.from_service_account_info(credentials_info)
    return credentials


def get_both_passed_users(user_data: Iterator) -> pd.DataFrame:
    df = pd.DataFrame(user_data)
    part1 = df.iloc[:, :7]
    return part1

def column_transformations(df: pd.DataFrame) -> pd.DataFrame:
    df["user_name"] = df["Email Address"].apply(lambda x: x.split('@')[0])
    df["user_name"]=df["user_name"].apply(lambda x: x.split('.')[0])
    df["user_name"]=df["user_name"].str.capitalize()
    df["company_name"]=df["Email Address"].apply(lambda x: x.split('@')[-1])
    df["Timestamp"]=df["Timestamp"].str[:9]
    df['Timestamp'] = df['Timestamp'].str.strip()

    return df

def transform_users_with_uid(df: pd.DataFrame) -> List[dict]:
    personal_info = []
    for i, row in df.iterrows():
        unique_user_id = generate_hash(row["Email Address"], SALT)

        user = {
            "certificate_holder_id": unique_user_id,
            "user_name": row["user_name"],
            "passed_at": row["Timestamp"],
            "level": row["Level"],
            "email": row["Email Address"],
            "score": row["Score"],
            "contact": row["Contact"],
            "last_name": row["Last Name"],
            "company_name": row["Company"]
        }
        personal_info.append(user)

    return personal_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="User Details Extractor",
        description="Generates JSONL file with extracted from Google Sheets user details.",
    )
    parser.add_argument(
        "output_file", type=str, help="Output file path, e.g. 'people.json'"
    )
    args = parser.parse_args()

    sheet_data = get_sheet(
        credentials=get_credentials(CREDENTIALS_INFO),
        spreadsheet_id=SHEET_ID,
        sheet_name=SHEET_NAME,
    )

    #print(list(sheet_data))
    #print(type(sheet_data))

    users_df = get_both_passed_users(sheet_data)
    users_df = column_transformations(users_df)
    users_info = transform_users_with_uid(users_df)
    print(f"{len(users_info)} users extracted")
    print(list(users_info))
    print(type(users_info))
    save_info_as_json(users_info, args.output_file)
