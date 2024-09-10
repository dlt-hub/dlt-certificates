import argparse
import json
import os
from datetime import datetime
from typing import List

from generate_summary import create_summary_markdown
from generate_unique_id import generate_hash

SALT = os.getenv("SALT")


def generate_markdown_certificate(user_data):
    markdown_template = f"""
# Certificate of Achievement: {user_data['certificate_name']}

## Awarded to **{user_data['user_name']}**

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
- **GitHub**: {user_data['github']}
- **Contact**: {user_data['contact']}

## Comments
{user_data['user_name']} has successfully completed the {user_data['course']['name']} and demonstrated exceptional proficiency as a {user_data['certificate_name']}. We commend their dedication and expertise in the field.

---

For more information, please visit [{user_data['issuer']['name']}]({user_data['issuer']['url']}).
    """
    return markdown_template


def create_certificate_files(user_data_list, certificate_info, output_directory):
    import os

    os.makedirs(output_directory, exist_ok=True)
    today = datetime.today()
    all_info = []
    for user_data in user_data_list:
        user_data.update(certificate_info)
        # hash(course name + user uid + salt)
        user_data["certificate_id"] = generate_hash(
            f"{user_data['course']['name']}-{user_data['certificate_holder_id']}", SALT
        )

        user_data["certified_at"] = today.strftime("%B %Y")
        user_data["created_at"] = today.isoformat()

        markdown_content = generate_markdown_certificate(user_data)

        filename = os.path.join(output_directory, f"{user_data['certificate_id']}.md")
        with open(filename, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)

        all_info.append(user_data)

    return all_info


def read_jsonl(file_path: str) -> List[dict]:
    with open(file_path) as f:
        data = json.load(f)
    return data


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
        "-o",
        "--output_directory",
        type=str,
        default="../certificates/technical_certification",
        help="Output file for generated certificates",
    )
    args = parser.parse_args()

    certificate_info = read_jsonl(args.certificate_info_file)
    users = read_jsonl(args.users_file)

    all_certificates_data = create_certificate_files(
        users, certificate_info, args.output_directory
    )
    create_summary_markdown(
        md_file_path="../README.md",
        certificate_data=all_certificates_data,
        regenerate=True,
    )
