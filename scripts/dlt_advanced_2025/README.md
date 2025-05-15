# dlt_advanced_2025 Certificate Generator

This folder contains scripts to generate certificates for dlt_advanced_2025 participants.

## Setup Instructions

1. Fill in the `.env` file with your Google Sheets credentials and information:
   - `SHEET_ID`: Your Google Sheet ID
   - `SHEET_NAME`: Name of the sheet tab containing participant data
   - `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google API credentials JSON file
   - `SALT`: A random string used for hashing participant IDs

2. Update `certificate_info.json` with your workshop details:
   - Workshop name, URL, and image
   - Issuer information
   - Certificate name and validity

## Usage

Run the following commands in order:

1. Load environment variables:
   ```
   source .env
   ```

2. Extract participant data from Google Sheets:
   ```
   python get_users_to_certificate.py workshop_users.json
   ```

3. Generate certificates:
   ```
   python generate_certificates.py workshop_users.json certificate_info.json
   ```

The certificates will be generated in the `certificates/technical_certification` directory.
