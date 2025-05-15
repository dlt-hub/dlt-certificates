import argparse
import json
from typing import List

stars = '<img src="certificates/badges/star.png" width="15">'


def create_summary_markdown(
    md_file_path: str, certificate_data: List[dict], regenerate: bool = False
) -> None:
    mode = "w" if regenerate else "a"

    with open(md_file_path, mode, encoding="utf-8") as file:
        # If regenerating, we write the headers first
        if regenerate:
            file.write("# Certificates\n\n")
            file.write(
                "| Certificate ID | Certificate Holder ID | Holder Name | Certificate Name | Level | Certified at | Valid Until | Holder GitHub | Contacts |\n"
            )
            file.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")

        # Write data for each certificate holder
        for data in certificate_data:
            file.write(
                f"| {data['certificate_id']} | {data['certificate_holder_id']} | {data['user_name']} | {data['certificate_name']} | {stars * data['level']} | {data['certified_at']} | {data['valid_until']} | {data['github']} | {data['contact']} |\n"
            )


def read_jsonl(file_path: str) -> List[dict]:
    with open(file_path) as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Certificate Generator",
        description="Generates Markdown file with a full list of certificate holders.",
    )
    parser.add_argument("users_file", type=str, help="JSON file with user data")
    parser.add_argument(
        "-r",
        "--regenerate",
        action="store_true",
        help="Regenerate all certificates based on `users_file`",
    )
    parser.add_argument(
        "-o",
        "--certificates_output_file",
        type=str,
        default="README.md",
        help="Output file for generated certificates",
    )
    args = parser.parse_args()

    users = read_jsonl(args.users_file)

    create_summary_markdown(args.certificates_output_file, users, args.regenerate)
