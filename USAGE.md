# PyForce Usage Guide

## Basic Examples

### Password Recovery
```bash
python PyForce.py --mode password_only --zip-file secret.zip --password-length 6 --password-lower --password-digits --max-attempts 5000
```

## Custom Character Sets
```bash
# Letters and numbers only
python PyForce.py --password-length 8 --password-lower --password-upper --password-digits

# Include special characters
python PyForce.py --password-length 10 --password-lower --password-upper --password-digits --password-special
```
## All Available Options

### Modes

- ```--mode password_only``` - Crack passwords only

- ```--mode username_only``` - Crack usernames only

- ```--mode both``` - Crack both (simulated)

### Password Options

- ```--password-length``` - Password length to generate

- ```--password-lower``` - Include lowercase letters

- ```--password-upper``` - Include uppercase letters

- ```--password-digits``` - Include numbers

- ```--password-special``` - Include special characters

### Username Options

- ```--username-length``` - Username length to generate

- ```--username-lower``` - Include lowercase letters

- ```--username-upper``` - Include uppercase letters

- ```--username-digits``` - Include numbers

- ```--username-special``` - Include special characters

### Safety Options

- ```--max-attempts``` - Maximum attempts before stopping

- ```--dry-run``` - Test settings without real cracking

## Step-by-Step Example

```bash
#1 Create test file
echo "Test data" > test.txt
zip -P 'abc123' test.zip test.txt

#2 Dry run to test
python PyForce.py --dry-run --mode password_only --password-length 6 --password-lower --password-digits

#Real recovery
python PyForce.py --mode password_only --zip-file test.zip --password-length 6 --password-lower --password-digits --max-attempts 10000
```

## Tips

- Start with short lengths for testing

- Always use --max-attempts for safety

- Use --dry-run to verify settings first

- Combine character types for stronger attacks







