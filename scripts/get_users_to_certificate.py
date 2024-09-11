import argparse
import os
from typing import Any, Iterator, List

import pandas as pd
import pendulum
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from generate_unique_id import generate_hash
from utils import save_info_as_json

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
    part1 = df.iloc[:, :4]
    part2 = df.iloc[:, 4:7]
    both = part1.merge(
        part2, how="inner", left_on="email_part1", right_on="email_part2"
    ).drop_duplicates(subset=["email_part1"], keep="last")
    both["passed_at_part2"] = both["passed_at_part2"].apply(
        lambda x: pendulum.parse(x, strict=False).isoformat()
    )

    return both


def transform_users_with_uid(df: pd.DataFrame) -> List[dict]:
    personal_info = []
    for i, row in df.iterrows():
        unique_user_id = generate_hash(row["email_part2"], SALT)
        user = {
            "certificate_holder_id": unique_user_id,
            "user_name": row["full_name_part1"],
            "passed_at": row["passed_at_part2"],
            "github": "TBA",
            "contact": "TBA",
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

    users_df = get_both_passed_users(sheet_data)
    users_info = transform_users_with_uid(users_df)

    save_info_as_json(users_info, args.output_file)
