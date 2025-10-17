import argparse
import csv
import json
import os
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_json(chain, address, apikey, out):
    apikey = apikey.strip()  # Remove any whitespace/newlines
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Use Etherscan API V2
            res = requests.get(f"https://api.etherscan.io/v2/api?module=contract&action=getabi&address={address}&chainid={chain}&apikey={apikey}", verify=False, timeout=30).json()
            print(f"API Response for {address}: {res}")
            if not res["status"] == "1":
                raise Exception(f"Couldn't fetch ABI for contract {address} from Etherscan. Response: {res}")
            with open(out, 'w') as f:
                json.dump(json.loads(res["result"]), f, indent=2)
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {address}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"Failed to fetch ABI for {address} after {max_retries} attempts")
                return False

def main():
    parser = argparse.ArgumentParser(description='Fetch and store ABI files from a CSV list')
    parser.add_argument('-l', '--csv-list', help="the CSV list of tokens", default="abi_list.csv")
    parser.add_argument('-k', '--api-key', help="the Etherscan API key file", default=".etherscan_apikey")
    parser.add_argument('-o', '--output', help="the output directory", default="repo")
    args = parser.parse_args()

    api_key = None

    with open(args.api_key, 'r') as f:
        api_key = f.read()

    success_count = 0
    failure_count = 0
    
    with open(args.csv_list, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            output = os.path.join(args.output, f"{row[0]}.json")
            if not os.path.exists(output):
                print(f"Fetching ABI for {row[0]} ({row[2]})...")
                if fetch_json(row[1], row[2], api_key, output):
                    success_count += 1
                else:
                    failure_count += 1
            else:
                print(f"ABI for {row[0]} already exists, skipping...")
                success_count += 1
    
    print(f"\nSummary: {success_count} successful, {failure_count} failed")

if __name__ == "__main__":
    main()