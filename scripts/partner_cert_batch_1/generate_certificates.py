import argparse
import os
from typing import List

import pendulum

from generate_summary import create_summary_markdown
from utils import generate_hash, read_jsonl, save_info_as_json

SALT = os.getenv("SALT")

stars = '<img src="../badges/star.png" width="48">'


def generate_markdown_certificate(user_data: dict) -> str:
    markdown_template = f"""
# Certificate of Achievement: {user_data['certificate_name']}

## Awarded to {user_data['user_name']} {user_data['last_name']}

![Course Image]({user_data['course']['image_url']})

### Certificate Details
- **Certificate ID**: `{user_data['certificate_id']}`
- **Certificate Holder ID**: `{user_data['certificate_holder_id']}`

### Course Information
- **Course**: [{user_data['course']['name']}]({user_data['course']['url']})

### Issued by
[**{user_data['issuer']['name']}**]({user_data['issuer']['url']}) 

### Certification Period
- **Issued**: {user_data['certified_at']}
- **Valid Until**: {user_data['valid_until']}

---

## Contact Information
- **Contact**: {user_data['contact']}

---

For more information, please visit [{user_data['issuer']['name']}]({user_data['issuer']['url']}).
    """
    return markdown_template


def create_certificate_files(
    user_data_list: List[dict], certificate_info: dict, output_directory: str
) -> List[dict]:
    os.makedirs(output_directory, exist_ok=True)
    today = pendulum.today()
    all_info = []
    for user_data in user_data_list:
        user_data.update(certificate_info)
        # hash(course name + user uid + salt)
        user_data["certificate_id"] = generate_hash(
            f"{user_data['course']['name']}-{user_data['certificate_holder_id']}", SALT
        )

        user_data["certified_at"] = pendulum.parse(user_data["passed_at"], strict=False).strftime(
            "%B %Y"
        )
        user_data["created_at"] = today.isoformat()

        comment = ""
        if user_data["level"] == 3:
            comment = f" and demonstrated exceptional proficiency as a {user_data['certificate_name']}"
        user_data["level_comment"] = comment

        markdown_content = generate_markdown_certificate(user_data)

        filename = os.path.join(output_directory, f"{user_data['certificate_id']}.md")
        with open(filename, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)

        all_info.append(user_data)

    return all_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Certificate Generator",
        description="Generates Markdown formatted certificate based on the provided data structure.",
    )
    parser.add_argument("users_file", type=str, help="JSON file with user data")
    parser.add_argument(
        "certificate_info_file", type=str, help="JSON file with certificate info"
    )
    parser.add_argument(
        "-od",
        "--output_directory",
        type=str,
        default="../certificates/technical_certification",
        help="Output file for generated certificates",
    )
    parser.add_argument(
        "-r",
        "--regenerate",
        action="store_true",
        help="Regenerate certificates summary based on `users_file`",
    )
    parser.add_argument(
        "-osf",
        "--output_summary_file",
        type=str,
        default="../README.md",
        help="Output file for generated certificates summary",
    )
    args = parser.parse_args()

    certificate_info = read_jsonl(args.certificate_info_file)
    users = read_jsonl(args.users_file)

    all_certificates_data = create_certificate_files(
        users, certificate_info, args.output_directory
    )
    create_summary_markdown(
        md_file_path=args.output_summary_file,
        certificate_data=all_certificates_data,
        regenerate=args.regenerate,
    )
    print(f"{len(all_certificates_data)} certificates generated successfully.")
    save_info_as_json(all_certificates_data, "./all_certificates_data.json")

    import pandas

    df = pandas.DataFrame(all_certificates_data)
    df["First Name"] = df["user_name"].apply(lambda x: x.split(" ")[0])
    df["Last Name"] = df["last_name"]
    df_part = df.loc[
        :,
        (
            "certificate_holder_id",
            "certificate_id",
            "certificate_name",
            "First Name",
            "email",
        ),
    ]
    df_part.to_csv(f"to_active_campaign_{pendulum.today()}.csv", index=False)