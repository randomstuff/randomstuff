#!/usr/bin/python3

import sys
import json
import argparse

import yaml

parser = argparse.ArgumentParser(description='Convert YAML to JSON.')
parser.add_argument('filename', metavar='FILE', type=str, nargs='?',
                    help='Input YAML files')
parser.add_argument('--pretty', action='store_true', default=False, help='Pretty print')
args = parser.parse_args()

if args.filename is None:
    data = yaml.safe_load(sys.stdin)
else:
    with open(args.filename, "rt") as f:
        data = yaml.safe_load(f)

if args.pretty:
    indent = "  "
else:
    indent = None

sys.stdout.write(json.dumps(data, indent=indent))
