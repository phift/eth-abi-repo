#!/usr/bin/env python3
"""
Script to deduplicate ABIs and create a clean collection with unique ABIs only.
Since the tool matches by ABI rather than address, we only need one representative
of each unique ABI type.
"""

import json
import hashlib
import argparse
from datetime import datetime
from collections import defaultdict

def is_erc20(abi):
    """Check if ABI matches ERC20 standard"""
    functions = [item for item in abi if item.get('type') == 'function']
    function_names = [f.get('name', '') for f in functions]
    
    # Core ERC20 functions
    erc20_functions = ['transfer', 'approve', 'balanceOf', 'totalSupply', 'allowance', 'transferFrom']
    return all(name in function_names for name in erc20_functions)

def is_erc721(abi):
    """Check if ABI matches ERC721 standard"""
    functions = [item for item in abi if item.get('type') == 'function']
    function_names = [f.get('name', '') for f in functions]
    
    # Core ERC721 functions
    erc721_functions = ['ownerOf', 'transferFrom', 'approve', 'balanceOf', 'safeTransferFrom']
    return all(name in function_names for name in erc721_functions)

def deduplicate_abis(input_file, output_file):
    """Deduplicate ABIs and create clean collection"""
    
    # Load the current ABI collection
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    abis = data['abis']
    print(f'Original ABIs: {len(abis)}')
    
    # Group ABIs by their hash to find duplicates
    abi_groups = defaultdict(list)
    for i, abi in enumerate(abis):
        abi_str = json.dumps(abi, sort_keys=True)
        abi_hash = hashlib.md5(abi_str.encode()).hexdigest()
        abi_groups[abi_hash].append(i)
    
    # Create deduplicated list (keep first occurrence of each unique ABI)
    deduplicated_abis = []
    seen_hashes = set()
    
    erc20_found = False
    erc721_found = False
    
    for i, abi in enumerate(abis):
        abi_str = json.dumps(abi, sort_keys=True)
        abi_hash = hashlib.md5(abi_str.encode()).hexdigest()
        
        if abi_hash not in seen_hashes:
            seen_hashes.add(abi_hash)
            
            # Check if this is ERC20 or ERC721
            if is_erc20(abi) and not erc20_found:
                print(f'Including ERC20 ABI (index {i})')
                deduplicated_abis.append(abi)
                erc20_found = True
            elif is_erc721(abi) and not erc721_found:
                print(f'Including ERC721 ABI (index {i})')
                deduplicated_abis.append(abi)
                erc721_found = True
            elif not is_erc20(abi) and not is_erc721(abi):
                # Include non-standard ABIs
                deduplicated_abis.append(abi)
    
    # Create new data structure
    t = datetime.now()
    new_data = {
        "version": t.strftime("%Y%m%d"),
        "timestamp": int(t.timestamp()),
        "abis": deduplicated_abis
    }
    
    # Save deduplicated collection
    with open(output_file, 'w') as f:
        json.dump(new_data, f, indent=2)
    
    print(f'Deduplicated ABIs: {len(deduplicated_abis)}')
    print(f'ERC20 included: {erc20_found}')
    print(f'ERC721 included: {erc721_found}')
    print(f'Saved to: {output_file}')

def main():
    parser = argparse.ArgumentParser(description='Deduplicate ABI collection')
    parser.add_argument('-i', '--input', help='Input ABI JSON file', default='build/abi.json')
    parser.add_argument('-o', '--output', help='Output ABI JSON file', default='build/abi_deduplicated.json')
    args = parser.parse_args()
    
    deduplicate_abis(args.input, args.output)

if __name__ == "__main__":
    main()
