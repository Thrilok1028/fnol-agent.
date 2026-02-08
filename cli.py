#!/usr/bin/env python3
"""
Synapx FNOL Agent - Command Line Interface
Usage: python cli.py samples/acord_sample.txt
"""
import sys
import json
from fnol_agent import process_file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cli.py <path-to-fnOL-file>")
        print("Example: python cli.py samples/acord_sample.txt")
        sys.exit(1)
    
    try:
        result = process_file(sys.argv[1])
        print(json.dumps(result, indent=2))
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)
