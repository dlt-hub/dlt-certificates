# Generate Certificates

## Table of Contents

- [Overview](#overview)
- [User Details Extractor](#user-details-extractor)
- [Generating Markdown Certificates](#generating-markdown-certificates)
- [Generating Certificates Summary](#generating-certificates-summary)

## Overview
This guide describes how to generate certificates from user data extracted automatically 
from Google Sheets and generate a structured Markdown file listing certificate holders.


## User Details Extractor
The script `scripts/get_users_to_certificate.py` is used to extract participant data from a Google Sheet, 
which is linked to Google Form, and generates a JSONL file formatted as [below](#output-format).

#### Generating Unique IDs
To generate unique IDs for each certificate holder, the `generate_hash` function (from `scripts/generate_unique_id.py`) uses the [hashlib library](https://docs.python.org/3/library/hashlib.html).

### Running the Script
1. **Install dependencies**:
   ```shell
   pip install -U google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
1. **Set Up Credentials**:
   - Copy `example.env` to `.env`.
   - Populate `.env` with your credentials.
   - Run `set -a && source .env && set +a` to export the environment variables.
   - Share Spreadsheet with Google Service account: `dlt-google-sheets-...@...gserviceaccount.com`
2. **Execute the Script**:
   ```bash
   python scripts/get_users_to_certificate.py output_file_path_here.json
   ```
   This command will extract data from the specified Google Sheet, process it to generate unique IDs and certificate details, and save the output to `output_file_path_here.json`.

   `output_file_path_here.json` specifies the path where the extracted user details will be stored.
   
   For example:
   ```shell
   cd scripts && python get_users_to_certificate.py test_users.json
   ```
   
### Output Format
The script outputs a JSONL file where each line corresponds to a user's certificate information, including:

- Unique user and certificate IDs
- User's name, contact, and GitHub URL
- Date when the second Homework was done.
- Course details, issuer information, and certification period

Here's an example of what a line in the JSONL file might look like:

```json
[
  {
    "certificate_holder_id": "123099df0hhf0f8h8klh0ll009jkl9gd999h3h5",
    "user_name": "Alice Johnson",
    "level": 3,
    "passed_at": "2024-08-30T18:04:44+00:00",
    "github": "https://github.com/alicejohnson",
    "contact": "https://www.linkedin.com/in/alicejohnson"
  },
  // Additional records...
]
```

## Generating Markdown Certificates

The `scripts/generate_certificates.py` script automates the creation of personalized certificates in Markdown format. 
It reads user data from a JSON file and generates a Markdown file for each user with a detailed certificate.

The certificates include details like the user's name, the course they've completed, 
the issuing authority, and a unique certificate ID. 
The script also provides an option to regenerate a summary of all generated certificates.

### Usage

To use the script, you must have a **JSON file with user data** structured according to the expected format (see [above](#output-format) for format details)
and **JSON file with certification data** with format:
```json
{
    "course": {
        "name": "Workshop: ELT with DLT",
        "url": "https://github.com/dlt-hub/dlthub-education/tree/main/workshops/workshop_august_2024",
        "image_url": "../badges/advanced_etl_specialist.png"
    },
    "issuer": {"name": "dltHub", "url": "https://dlthub.com/"},
    "certificate_name": "dlt Advanced ELT Specialist",
    "valid_until": "No expiration"
}
```
The script is run from the command line as follows:

```bash
python generate_certificates.py <users_file> <certificate_info_file> [options]
```

### Command Line Arguments

#### Arguments

- `<users_file>`: Path to the JSON file containing user data.
- `<certificate_info_file>`: Path to the JSON file containing certificate info.

#### Options

- `-od, --output_directory`: Path where the generated certificates will be stored. Default is `../certificates/technical_certification`.
- `-r, --regenerate`: If this flag is set, the script regenerates the certificates summary based on the `users_file`.
- `-osf, --output_summary_file`: Path where the summary file of all generated certificates will be written. Default is `../README.md`.
- 
## Output

1. **Generated Certificate**: A markdown file will be created for each user in the specified output directory, named using the `certificate_id` of each user.
2. **Certificate Summary**: An optional markdown summary file can be updated or re-created if the `--regenerate` flag is used.

### Example

Running the script with an example command:

```bash
cd scripts && python generate_certificates.py test_users.json certificate_info.json -od ../certificates/technical_certification -r -osf ../README.md
```

This will read `test_users.json`, generate Markdown certificates for each user in the JSON file, 
and save them in the `./certificates/technical_certification` directory.


## Generating Certificates Summary

The `scripts/generate_summary.py` script processes JSON-formatted user data to create a Markdown document listing certificate holders.

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
python generate_summary.py test_users.json
```

Regenerate the Markdown file:
```bash
python generate_summary.py test_users.json -r
```

Specify a different output file:
```bash
python generate_summary.py test_users.json -o output.md
```

### Input Format
Ensure your JSON file matches the structure as follows:
```json
[
    {
        "certificate_holder_id": "123099df0hhf0f8h8klh0ll009jkl9gd999h3h5",
        "user_name": "Alice Johnson",
        "level": 3,
        "github": "https://github.com/alicejohnson",
        "contact": "https://www.linkedin.com/in/alicejohnson",
        "course": {
            "name": "Workshop: ELT with DLT",
            "url": "https://github.com/dlt-hub/dlthub-education/tree/main/workshops/workshop_august_2024",
            "image_url": "../badges/advanced_etl_specialist.png"
        },
        "issuer": {
            "name": "dltHub",
            "url": "https://dlthub.com/"
        },
        "certificate_name": "dlt Advanced ELT Specialist",
        "valid_until": "No expiration",
        "certificate_id": "3951e4f32af466f7dfec5a1053f4d0ac5f2d7143c599d7ada2b6bff0e28e4521",
        "certified_at": "September 2024",
        "created_at": "2024-09-11T16:53:02.417924"
    },
```

### Output Format
The script outputs a Markdown file with certificate details formatted in a table with headers: "Certificate ID", "Certificate Holder ID", "Holder Name", "Certificate Name", "Certified at", "Valid Until", "Holder GitHub", and "Contacts".
