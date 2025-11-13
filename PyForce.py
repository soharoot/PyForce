#!/usr/bin/env python3
"""
EDUCATIONAL BRUTE-FORCE SIMULATION TOOL
FOR SECURITY LEARNING IN SAFE LAB ENVIRONMENTS ONLY
"""

import argparse
import itertools
import string
import time
import sys
import os
import zipfile
from typing import List, Tuple, Optional

LEGAL_NOTICE = """
*******************************************************************************
                      EDUCATIONAL SECURITY TOOL - LEGAL NOTICE
*******************************************************************************

THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY IN CONTROLLED LAB ENVIRONMENTS.

IMPORTANT LEGAL AND ETHICAL CONSTRAINTS:
- DO NOT use this tool on any systems, services, or accounts you do not own
- DO NOT use this tool without explicit written permission from the system owner
- DO NOT use this tool against any production systems or real user accounts
- This tool operates ONLY on local, user-provided test data
- The author accepts NO RESPONSIBILITY for misuse of this tool

By proceeding, you confirm that:
1. You will use this tool only in your own lab environment
2. You understand the legal consequences of unauthorized testing
3. You accept full responsibility for your use of this tool
4. You are using this tool for legitimate educational purposes

*******************************************************************************
"""

class BruteForceSimulator:
    def __init__(self):
        self.attempts = 0
        self.start_time = 0
        self.found_credentials = None
        
    def get_character_set(self, include_digits: bool, include_lower: bool, 
                         include_upper: bool, include_special: bool) -> str:
        charset = ""
        if include_digits:
            charset += string.digits
        if include_lower:
            charset += string.ascii_lowercase
        if include_upper:
            charset += string.ascii_uppercase
        if include_special:
            charset += string.punctuation
            
        if not charset:
            raise ValueError("At least one character type must be selected")
        return charset
    
    def calculate_search_space(self, length: int, charset: str, max_attempts: Optional[int] = None) -> Tuple[int, float]:
        total_combinations = len(charset) ** length
        if max_attempts and max_attempts < total_combinations:
            total_combinations = max_attempts
        estimated_time = total_combinations / 1000  
        return total_combinations, estimated_time
    
    def generate_candidates(self, length: int, charset: str, max_attempts: Optional[int] = None):
        generated = 0
        for candidate in itertools.product(charset, repeat=length):
            if max_attempts and generated >= max_attempts:
                break
            yield ''.join(candidate)
            generated += 1

    def test_zip_password(self, zip_path: str, password: str) -> bool:
        """Test if password can open the zip file"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(pwd=password.encode(), path='/tmp/zip_test')
                return True
        except:
            return False

    def crack_zip_file(self, zip_file: str, username_params: dict, password_params: dict, 
                      max_attempts: int, mode: str):
        """Crack username and password for a zip file"""
        print(f"\n🔓 Starting ZIP file attack on: {zip_file}")
        print(f"Mode: {mode}")
        print(f"Max attempts: {max_attempts:,}")
        
        self.attempts = 0
        self.start_time = time.time()
        self.found_credentials = None
        
        if mode == "username_only":
            self._crack_zip_username_only(zip_file, username_params, max_attempts)
        elif mode == "password_only": 
            self._crack_zip_password_only(zip_file, password_params, max_attempts)
        else:  # both
            self._crack_zip_both(zip_file, username_params, password_params, max_attempts)
            
        return self.found_credentials

    def _crack_zip_password_only(self, zip_file: str, params: dict, max_attempts: int):
        """Crack only the password (assume username is known)"""
        charset = self.get_character_set(params['digits'], params['lower'], 
                                       params['upper'], params['special'])
        total_estimated, _ = self.calculate_search_space(params['length'], charset, max_attempts)
        
        print(f"Password search space: {total_estimated:,} combinations")
        
        for i, password in enumerate(self.generate_candidates(params['length'], charset, max_attempts)):
            self.attempts = i + 1
            
            if i % 100 == 0:
                elapsed = time.time() - self.start_time
                rate = i / elapsed if elapsed > 0 else 0
                print(f"Attempt {i:,} - Testing: '{password}' - Rate: {rate:.1f}/sec")
            
            if self.test_zip_password(zip_file, password):
                elapsed = time.time() - self.start_time
                print(f"\n✅ SUCCESS! Found password: '{password}'")
                print(f"Total attempts: {self.attempts:,}")
                print(f"Time elapsed: {elapsed:.2f} seconds")
                self.found_credentials = ("admin", password)  # Assuming admin as username
                return
                
            if i >= max_attempts:
                print(f"\n❌ Max attempts reached: {max_attempts:,}")
                return

    def _crack_zip_username_only(self, zip_file: str, params: dict, max_attempts: int):
        """Crack only the username (for demonstration)"""
        print("Username cracking for ZIP files is simulated (real implementation would need different target)")
        # In real scenario, you'd need a service that uses usernames
        charset = self.get_character_set(params['digits'], params['lower'],
                                       params['upper'], params['special'])
        
        for i, username in enumerate(self.generate_candidates(params['length'], charset, max_attempts)):
            self.attempts = i + 1
            print(f"Testing username: '{username}'")
            
            if i >= 10:  # Just show a few examples
                print("Username cracking simulation complete")
                break

    def _crack_zip_both(self, zip_file: str, username_params: dict, password_params: dict, max_attempts: int):
        """Crack both username and password (simplified)"""
        print("Both username and password cracking - using password cracking only for ZIP files")
        return self._crack_zip_password_only(zip_file, password_params, max_attempts)

def dry_run(username_params: Optional[dict], password_params: dict, mode: str):
    print("\n🧪 DRY RUN - Candidate Generation Strategy")
    print("=" * 50)
    
    if mode == "username_only" and username_params:
        charset = simulator.get_character_set(username_params['digits'], 
                                            username_params['lower'],
                                            username_params['upper'], 
                                            username_params['special'])
        total, est_time = simulator.calculate_search_space(username_params['length'], charset)
        print(f"USERNAME GENERATION:")
        print(f"  Length: {username_params['length']}")
        print(f"  Character set: {charset}")
        print(f"  Total combinations: {total:,}")
        
        examples = list(itertools.islice(
            simulator.generate_candidates(username_params['length'], charset), 5))
        for ex in examples:
            print(f"    - {ex}")
    
    if mode in ["password_only", "both"] and password_params:
        charset = simulator.get_character_set(password_params['digits'], 
                                            password_params['lower'],
                                            password_params['upper'], 
                                            password_params['special'])
        total, est_time = simulator.calculate_search_space(password_params['length'], charset)
        print(f"\nPASSWORD GENERATION:")
        print(f"  Length: {password_params['length']}")
        print(f"  Character set: {charset}")
        print(f"  Total combinations: {total:,}")
        
        examples = list(itertools.islice(
            simulator.generate_candidates(password_params['length'], charset), 5))
        for ex in examples:
            print(f"    - {ex}")

def get_user_confirmation():
    print(LEGAL_NOTICE)
    response = input("Do you understand and accept these terms? (yes/NO): ").strip().lower()
    return response == 'yes'

def main():
    parser = argparse.ArgumentParser(
        description='Educational brute-force tool for ZIP files and other targets',
        epilog='''
EXAMPLES:
  # Crack a password-protected ZIP file
  %(prog)s --mode password --zip-file secret.zip --password-length 8 --password-digits --password-lower --max-attempts 10000
  
  # Dry run to see strategy
  %(prog)s --dry-run --mode password --password-length 4 --password-digits --lower
  
  # Crack both username and password (simulated)
  %(prog)s --mode both --zip-file protected.zip --username-length 5 --username-lower --password-length 6 --password-digits --password-lower
        '''
    )
    
    # Target specification
    target_group = parser.add_argument_group('Target Configuration')
    target_group.add_argument('--zip-file', type=str, help='Password-protected ZIP file to crack')
    
    # Mode selection
    mode_group = parser.add_argument_group('Attack Mode')
    mode_group.add_argument('--mode', choices=['username_only', 'password_only', 'both'], required=True, help='What to brute-force')
    
    # Username parameters
    username_group = parser.add_argument_group('Username Generation')
    username_group.add_argument('--username-length', type=int, default=4)
    username_group.add_argument('--username-digits', action='store_true')
    username_group.add_argument('--username-lower', action='store_true')
    username_group.add_argument('--username-upper', action='store_true')
    username_group.add_argument('--username-special', action='store_true')
    
    # Password parameters
    password_group = parser.add_argument_group('Password Generation')
    password_group.add_argument('--password-length', type=int, default=4)
    password_group.add_argument('--password-digits', action='store_true')
    password_group.add_argument('--password-lower', action='store_true')
    password_group.add_argument('--password-upper', action='store_true')
    password_group.add_argument('--password-special', action='store_true')
    
    # Safety limits
    safety_group = parser.add_argument_group('Safety Limits')
    safety_group.add_argument('--max-attempts', type=int, default=10000, help='Maximum attempts before stopping')
    
    # Operational modes
    operational_group = parser.add_argument_group('Operational Modes')
    operational_group.add_argument('--dry-run', action='store_true', help='Show strategy without executing')
    
    args = parser.parse_args()
    
    if not get_user_confirmation():
        print("Legal terms not accepted. Exiting.")
        return
    
    global simulator
    simulator = BruteForceSimulator()
    
    # Prepare parameters
    username_params = None
    password_params = None
    
    if args.mode in ['username_only', 'both']:
        username_params = {
            'length': args.username_length,
            'digits': args.username_digits,
            'lower': args.username_lower,
            'upper': args.username_upper,
            'special': args.username_special
        }
    
    if args.mode in ['password_only', 'both']:
        password_params = {
            'length': args.password_length,
            'digits': args.password_digits,
            'lower': args.password_lower,
            'upper': args.password_upper,
            'special': args.password_special
        }
    
    # Dry run mode
    if args.dry_run:
        dry_run(username_params, password_params, args.mode)
        return
    
    # Validate ZIP file exists
    if args.zip_file and not os.path.exists(args.zip_file):
        print(f"Error: ZIP file '{args.zip_file}' not found")
        return
    
    # Run the attack
    if args.zip_file:
        result = simulator.crack_zip_file(
            zip_file=args.zip_file,
            username_params=username_params,
            password_params=password_params,
            max_attempts=args.max_attempts,
            mode=args.mode
        )
        
        if result:
            username, password = result
            print(f"\n🎯 CRACKED CREDENTIALS:")
            print(f"Username: {username}")
            print(f"Password: {password}")
            print(f"\nUse these to open the ZIP file:")
            print(f"unzip {args.zip_file}")
        else:
            print(f"\n❌ Failed to crack the ZIP file")

if __name__ == "__main__":
    simulator = None
    try:
        main()
    except KeyboardInterrupt:
        print("\nAttack interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
