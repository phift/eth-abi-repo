import argparse
from datetime import datetime
import json
import os

def main():
    t = datetime.now()
    def_version = t.strftime("%Y%m%d")

    parser = argparse.ArgumentParser(description='Merge individual ABI JSON files into a single JSON')
    parser.add_argument('-i', '--input-dir', help="the CSV list of tokens", default="repo")
    parser.add_argument('-v', '--version', help="the version in YYYYMMDD format", default=def_version)
    parser.add_argument('-o', '--output', help="the output directory", default="build/abi.json")
    args = parser.parse_args()

    db = {"version" : args.version, "timestamp": int(t.timestamp()), "abis": []}

    for root, _, files in os.walk(args.input_dir):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file), 'r') as f:
                    db["abis"].append(json.load(f))
    
    os.makedirs(os.path.dirname(args.output))
    with open(args.output, 'w') as f:
        json.dump(db, f)


if __name__ == "__main__":
    main()