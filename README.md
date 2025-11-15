# PyForce - Educational Password Recovery Tool

> ⚠️ **LEGAL NOTICE**: For educational use and authorized testing only. Never use against systems you don't own.

## Installation

### Method 1: Direct Download
Download PyForce.py and run:
```bash
python PyForce.py --help
```
### Method 2: Git Clone
```bash
git clone https://github.com/soharoot/PyForce.git
cd PyForce
python PyForce.py --help
```
## Quick Start
```bash

# Create test ZIP file
echo "Secret data" > secret.txt
zip -P 'password123' secret.zip secret.txt

# Recover password
python PyForce.py --mode password_only --zip-file secret.zip --password-length 8 --password-lower --password-digits --max-attempts 10000
```
## Basic Usage
```bash
# Show help
python PyForce.py --help

# Dry run to test settings
python PyForce.py --dry-run --mode password_only --length 4 --lower --digits

# Crack ZIP password
python PyForce.py --mode password_only --zip-file protected.zip --password-length 6 --password-lower --password-upper --password-digits
```
## Features

- Real password recovery for ZIP files

- Custom character set generation

- Rate limiting and progress tracking

- Safety features and legal compliance
  
## Legal & Safety

ONLY USE IN:

- Your own lab environments

- Systems you explicitly own

- Educational exercises with permission
  
NEVER USE FOR:

- Unauthorized testing

- Malicious purposes

- Production systems







