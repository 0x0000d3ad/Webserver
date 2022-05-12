# Webserver
Webserver for contract metadata.

# Introduction
This simple webserver is designed to reveal metadata corresponding to NFT tokens that have been minted.  Querying for metadata for unminted tokens will result in the 'unrevealed' image metadata.  This allows projects to "reveal" their NFT's without exposing content for NFT's that have not been minted yet.

# Installation
Run pip to install the requirements in "requirements.txt"

> pin install -r requirements.txt

You will need to specify your contract abi in "data/abi.json".  Also, you must set some parameters in "data/appconfig.json", including:
1. Contract Address
2. Your infura mainnet link
3. The location of the unrevealed metadata
4. The location of the metadata

Finally, in webserver.py, you must specify the MAX_MINT, or max supply of tokens.  By default, the server will run on port 42525.  To change this, update the 'port' field in the function called from main.

# Running the server
Change directories to the root directory.  Run

> python3 webserver.py

# Querying for Metadata by tokenId

Assuming we are running on localhost, open a web browser and type the following URL into URL field:

> http://localhost:42525/tokenId?tokenId=1213

where you are free to change '1213' to the desired tokenId.
