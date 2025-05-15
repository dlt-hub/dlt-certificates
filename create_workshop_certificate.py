#!/usr/bin/env python3
"""
Workshop Setup Script

This script creates a new workshop folder with all necessary files
to generate certificates for course participants.
"""

import os
import shutil
import json
import sys
from pathlib import Path

# Define the base directory (the repository root)
BASE_DIR = Path(__file__).parent

def create_workshop_folder(workshop_name):
    """
    Create a new workshop folder with all necessary files.
    
    Args:
        workshop_name: Name of the workshop (will be used as directory name)
    """
    # Replace spaces with underscores and make lowercase for directory name
    folder_name = workshop_name.replace(" ", "_").lower()
    workshop_dir = BASE_DIR / "scripts" / folder_name
    
    # Make sure directory doesn't already exist
    if os.path.exists(workshop_dir):
        print(f"⚠️  Warning: Workshop directory '{folder_name}' already exists!")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            print("Operation cancelled.")
            return False
        
    # Create the directory
    os.makedirs(workshop_dir, exist_ok=True)
    print(f"✅ Created workshop directory: {workshop_dir}")
    
    # Define template files to copy from data_engineering_with_python
    template_files = [
        "generate_certificates.py",
        "get_users_to_certificate.py", 
        "users_info.py",
        "markdown_template.py",
    ]
    
    # Copy files from template directory
    template_dir = BASE_DIR / "scripts" / "data_engineering_with_python"
    for file in template_files:
        source = template_dir / file
        destination = workshop_dir / file
        shutil.copy2(source, destination)
        print(f"✅ Copied {file}")
    
    # Create certificate_info.json template
    certificate_info = {
        "course": {
            "name": workshop_name,
            "url": "https://github.com/yourusername/yourrepo",
            "image_url": "../badges/default_badge.png"
        },
        "issuer": {"name": "Your Organization", "url": "https://yourorganization.com/"},
        "certificate_name": "Certificate of Completion",
        "valid_until": "No expiration"
    }
    
    with open(workshop_dir / "certificate_info.json", 'w') as f:
        json.dump(certificate_info, f, indent=4)
    print(f"✅ Created certificate_info.json template")
    
    # Create .env template
    env_content = """SHEET_ID=<your_google_sheet_id>
SHEET_NAME=<your_sheet_name>
GOOGLE_APPLICATION_CREDENTIALS=<path_to_creds.json>
SALT=<random_string_for_hashing>
"""
    
    with open(workshop_dir / ".env", 'w') as f:
        f.write(env_content)
    print(f"✅ Created .env template")
    
    # Create README with instructions
    readme_content = f"""# {workshop_name} Certificate Generator

This folder contains scripts to generate certificates for {workshop_name} participants.

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
"""
    
    with open(workshop_dir / "README.md", 'w') as f:
        f.write(readme_content)
    print(f"✅ Created README.md with instructions")
    
    return True

def main():
    print("=" * 50)
    print("Workshop Certificate Generator Setup")
    print("=" * 50)
    
    workshop_name = input("Enter the name of your workshop: ")
    if not workshop_name:
        print("Workshop name cannot be empty. Exiting.")
        sys.exit(1)
    
    if create_workshop_folder(workshop_name):
        folder_name = workshop_name.replace(" ", "_").lower()
        print("\n✨ Setup complete! ✨")
        print(f"\nYour workshop files are in: scripts/{folder_name}/")
        print("\nNext steps:")
        print("1. Navigate to your workshop directory:")
        print(f"   cd scripts/{folder_name}/")
        print("2. Edit the .env and certificate_info.json files")
        print("3. Run the scripts as outlined in the README.md file")

if __name__ == "__main__":
    main() 