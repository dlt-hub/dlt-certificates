import argparse
import os
import sys
from typing import Any, Iterator

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from users_info import generate_users_info

sys.path.append(os.path.abspath("../"))
from legacy.utils import save_info_as_json


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="User Details Extractor",
        description="Generates JSONL file with extracted from Google Sheets user details.",
    )
    parser.add_argument(
        "output_file", type=str, help="Output file path, e.g. 'people.json'"
    )
    parser.add_argument("--env_path", default=".env", type=str, help="Env file path")
    args = parser.parse_args()

    load_dotenv(args.env_path)
    # set -a && source .env && set +a
    SHEET_ID = os.getenv("SHEET_ID")
    SHEET_NAME = os.getenv("SHEET_NAME")
    CREDENTIALS_INFO = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    SALT = os.getenv("SALT")

    sheet_data = get_sheet(
        credentials=get_credentials(CREDENTIALS_INFO),
        spreadsheet_id=SHEET_ID,
        sheet_name=SHEET_NAME,
    )

    users_info = generate_users_info(sheet_data, SALT)
    print(f"{len(users_info)} users extracted")
    save_info_as_json(users_info, args.output_file)
