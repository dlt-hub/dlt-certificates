import json
import os
from datetime import datetime
from typing import Any, Iterator, List

from generate_unique_id import generate_hash
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

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


def get_both_passed_users(user_data: Iterator, certificates_data: dict) -> List[dict]:
    emails_names = {}
    passed = []
    for row in user_data:
        emails_names[row.get("email_part1")] = row.get("full_name")
        if row.get("email_both"):
            passed.append(row.get("email_both"))

    personal_info = []
    for email in passed:
        unique_id = generate_hash(email, SALT)
        user = {
            "certificate_holder_id": unique_id,
            "user_name": emails_names[email],
            "github": "TBA",
            "contact": "TBA",
        }
        user.update(certificates_data)
        personal_info.append(user)

    return personal_info


def save_info_as_json(file_path: str, data: List[dict]) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    people_path = "people.json"

    today = datetime.today()

    certificate_info = {
        "course_name": "Workshop: ELT with DLT",
        "certificate_name": "dlt Advanced ELT Specialist",
        "certified_at": today.strftime("%B %Y"),
        "valid_until": "No expiration",
        "created_at": today.isoformat(),
    }

    sheet_data = get_sheet(
        credentials=get_credentials(CREDENTIALS_INFO),
        spreadsheet_id=SHEET_ID,
        sheet_name=SHEET_NAME,
    )

    users_info = get_both_passed_users(sheet_data, certificate_info)

    save_info_as_json(people_path, users_info)
