# ETH ABI Repository

This repository contains a selection of Ethereum SmartContract ABI descriptions in JSON format. These are fetched from [Etherscan](https://etherscan.io/) according to the `abi_list.csv` file in this repository and are saved to the `repo` directory of this repository.

`abi_list.csv` is a CSV file where each line is an entry. Its format is as follows

```csv
name,chainId,contractAddress,description
```

- `name`: a descriptive name of the ABI, this becomes the name of the saved JSON file
- `chainId`: the Chain ID where the contract is deployed
- `contractAddress`: the address of the contract to fetch the ABI, in case we are interested in a specific ERC this address can be of any contract fully implementing the ERC
- `description`: an additional comment, usually the contract name. This field is ignored

adding a ABI to this repository is done by adding a line to this file and running the `fetch_abi.py` script.

The script `build_abi.py` takes all JSON from the `repo` and generates a single file with all of them.

Feel free to use this repository however you like and to propose additions to the list. However since the purpose of this repository is to create an ABI database for [Keycard Shell](https://github.com/keycard-tech/keycard-shell) we will want to keep this list relatively short to fit the device memory.
