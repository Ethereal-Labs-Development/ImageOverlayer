# Description
# -----------------
# functionality for interfacing with our smart contract

# Resources
# -----------------
# Sign a Contract Txn: https://web3py.readthedocs.io/en/stable/web3.eth.account.html#sign-a-contract-transaction
#

from web3 import Web3
from web3.auto import w3
import json
import os


# contact address and contract abi for creating contract object
contract_address = "0xf0775e5a21e6f17009304D6565E9434977f938aE"
with open("contract_abi.json", "r") as f:
    contract_abi = json.load(f)

# create contract object
network = "ropsten"
w3 = Web3(Web3.HTTPProvider(f'https://{network}.infura.io/v3/4dd6cccb7c6c4c7a9a01f8b02b1ada03'))
nft_contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def get_new_token_id():
    """
    Returns the next available token via interacting with the contract.

    :return:
    """

    # print(nft_contract.all_functions())   # shows names of all functions on contract
    # print(nft_contract.functions.name().call())
    # print(nft_contract.functions.balanceOf('0x42A5243D51176bdCED13F40E3C85b7259e84c113').call())
    # print(nft_contract.functions.tokenURI(2).call())

    # TODO: function will be removed when a get_token function is added to the smart contract
    return 9    # CHANGE THIS


def mint_nft(to_address, uri):

    # get nonce for transaction
    nonce = w3.eth.get_transaction_count(to_address)

    token_id = get_new_token_id()

    # build the transaction
    mint_txn = nft_contract.functions.mint(
        to_address,     # owner of newly minted NFT
        token_id,       # unique identifier for the NFT
        uri,            # hosted link of JSON metadata
    ).buildTransaction({
        'chainId': 3,   # 3 is for ropsten, 1 is for mainnet
        'gas': 70000,
        'maxFeePerGas': w3.toWei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    # sign the transaction
    private_key = os.environ['PK']
    signed_txn = w3.eth.account.sign_transaction(mint_txn, private_key=private_key)

    # broadcast the transaction
    bc_txn = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(bc_txn)


if __name__ == "__main__":
    # my_address = '0x4dE801A18FaA4268eBe916F132CcD760b7C649B9'
    my_address = '0x42A5243D51176bdCED13F40E3C85b7259e84c113'
    print(nft_contract.functions.balanceOf(my_address).call())
    uri = "https://gateway.pinata.cloud/ipfs/Qmc7yWr8Q8j3fWJMK6zcwUEYPUcigeTDbBca857xD7Sg5Q"    # JSON
    mint_nft(my_address, uri)
    print(nft_contract.functions.balanceOf(my_address).call())