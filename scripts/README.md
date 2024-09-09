# Generate Certificates

## Table of Contents

- [Overview](#overview)
- [Preparing User Data](#preparing-user-data)
- [Generating Markdown Certificates](#generating-markdown-certificates)
- [Generating Certificates Summary](#generating-certificates-summary)

## Overview
This guide describes how to generate certificates from user data extracted automatically 
from Google Sheets and generate a structured Markdown file listing certificate holders.

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

### User Details Extractor
The script `scripts/get_users_to_certificate.py` is used to extract participant data from a Google Sheet, which is linked to Google Form, and generates a JSONL file formatted as shown above.

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
- Course details, issuer information, and certification period

Here's an example of what a line in the JSONL file might look like:

```json
{
  "certificate_id": "generated_certificate_id_here",
  "certificate_holder_id": "generated_user_id_here",
  "user_name": "John Doe",
  "github": "https://github.com/johndoe",
  "contact": "https://www.linkedin.com/in/johndoe",
  "course": {
    "name": "Workshop: ELT with DLT",
    "url": "https://github.com/dlt-hub/dlthub-education/tree/main/workshops/workshop_august_2024",
    "image_url": ""
  },
  "issuer": {
    "name": "dltHub",
    "url": "https://dlthub.com/"
  },
  "certificate_name": "dlt Advanced ELT Specialist",
  "certified_at": "September 2024",
  "valid_until": "No expiration",
  "created_at": "2024-09-09T18:11:04.710717"
}
```

## Generating Markdown Certificates

The `scripts/generate_certificates.py` script automates the creation of personalized certificates in Markdown format. 
It reads user data from a JSON file and generates a Markdown file for each user with a detailed certificate.

### Usage

To use the script, you must have a JSON file with user data structured according to the expected format (see [above](#data-structure) for format details). 
The script is run from the command line as follows:

```bash
python generate_certificates.py [path_to_user_data_file] -o [output_directory]
```

### Command Line Arguments

- `users_file`: Specifies the path to the JSON file containing user data.
- `-o`, `--output_directory`: (Optional) Specifies the directory where the certificate Markdown files will be saved. Default is `../certificates/technical_certification`.

### Output

The script generates a Markdown file for each entry in the JSON file. 
These files are saved to the specified output directory, named using the `certificate_id` of each user.

### Example

Running the script with an example command:

```bash
cd scripts && python generate_certificates.py test_users.json -o ../certificates/technical_certification
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
Ensure your JSON file matches the structure provided in the **[Data Structure](#data-structure)** section.

### Output Format
The script outputs a Markdown file with certificate details formatted in a table with headers: "Certificate ID", "Certificate Holder ID", "Holder Name", "Certificate Name", "Certified at", "Valid Until", "Holder GitHub", and "Contacts".
