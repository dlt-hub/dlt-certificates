# Generate Certificates

## Overview
This guide describes how to generate certificates from user data extracted automatically from Google Sheets and generate a structured Markdown file listing certificate holders.

## Preparing User Data

### Data Structure
Ensure your data conforms to the following JSON structure:
```json
[
    {
        "certificate_id": "c5989d5ffg09hf9dg90hfg90h0fg4c3deebb27a",
        "certificate_holder_id": "682099if0ggf0f9h9ngh0hg009hgh9gd617b2",
        "user_name": "First_Name Last_Name",
        "github": "GitHub account url (e.g. https://github.com/gvanrossum)",
        "contact": "Any contact details (e.g. Linkedin url)",
        "course": {
            "name": "Workshop: ELT with DLT",
            "url": "https://github.com/dlt-hub/dlthub-education/tree/main/workshops/workshop_august_2024",
            "image_url": ""
        },
        "issuer": {
            "name": "dltHub", 
            "url": "https://dlthub.com/"
        },
        "certificate_name": "Certificate name (e.g. dlt Advanced ELT Specialist)",
        "certified_at": "Month Year (e.g. September 2024)",
        "valid_until": "Month Year (or No expiration)",
        "created_at": "2024-09-09T11:32:05.776872"
    },
    // Additional records...
]
```

### Extracting Data
The script `workshop_certification/get_users_to_certificate.py` is used to extract participant data from a Google Sheet, which is linked to Google Form, and generates a JSONL file formatted as shown above.

#### Generating Unique IDs
To generate unique IDs for each certificate holder, the `generate_hash` function (from `workshop_certification/generate_unique_id.py`) uses the [hashlib library](https://docs.python.org/3/library/hashlib.html).

### Running the Script
1. **Set Up Credentials**:
   - Rename `example.env` to `.env`.
   - Populate `.env` with your credentials.
   - Run `set -a && source .env && set +a` to export the environment variables.

2. **Execute the Script**:
   ```bash
   python workshop_certification/get_users_to_certificate.py people.json
   ```
   `people.json` specifies the path where the extracted user details will be stored.

## Generating Markdown Certificates

The `generate_summary.py` script processes JSON-formatted user data to create a Markdown document listing certificate holders.

### Features
- Generates a detailed list of certificate holders in Markdown format.
- Supports appending to or regenerating the Markdown document.
- Efficiently processes JSON input.

### Usage

#### Command Line Arguments
- `users_file`: Path to the JSON file containing user data (required).
- `-r`, `--regenerate`: Completely regenerate the Markdown file using the specified JSON data.
- `-o`, `--certificates_output_file`: Path for the generated Markdown file (default is `README.md`).

#### Examples
Append to an existing Markdown file:
```bash
python generate_summary.py users_data.json
```

Regenerate the Markdown file:
```bash
python generate_summary.py users_data.json -r
```

Specify a different output file:
```bash
python generate_summary.py users_data.json -o output.md
```

### Input Format
Ensure your JSON file matches the structure provided in the **Data Structure** section.

### Output
The script outputs a Markdown file with certificate details formatted in a table with headers: "Certificate Holder ID", "Holder Name", "Certificate Name", "Certified at", "Valid Until", "Holder GitHub", and "Contacts".
