#!/usr/bin/env python3
"""
Simple test runner for the display_utils test suite
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print the results"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode

def main():
    """Run various test configurations"""
    
    # Change to test directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)

    print("Display Utils Test Suite Runner")
    print("==============================")
    
    # Run tests with different configurations
    commands = [
        ("pytest test_display_utils.py -v", "Running all tests with verbose output"),
        ("pytest test_display_utils.py --cov=display_utils --cov-report=term-missing", "Running tests with coverage report"),
    ]
    
    failed = False
    for cmd, desc in commands:
        returncode = run_command(cmd, desc)
        if returncode != 0:
            failed = True
    
    if failed:
        print("\n❌ Some tests failed!")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
