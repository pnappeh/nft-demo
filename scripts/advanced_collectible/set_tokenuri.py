from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import get_ring_owner, get_account, OPENSEA_URL

ring_owner_metadata_dic = {
    "GANDALF": "https://ipfs.io/ipfs/QmSXq2rPYs7Ec9FbpNp1k96apsApBFkZkcXgvCuKQQUcCx?filename=0-GANDALF.json",
    "NAZGUL": "https://ipfs.io/ipfs/QmbjVQ7qbmT6o5R1oYgFQ8jQp9sM1T6cusbPwR3s3tFwsG?filename=0-NAZGUL.json",
    "SAURON": "https://ipfs.io/ipfs/QmYKPuTzFPvnK6t4VM1v1RDPiGRmEuQGVy1jmcsnHfws7x?filename=0-SAURON.json",
}
ring_owner_metadata_pinata_dic = {
    "GANDALF": "https://gateway.pinata.cloud/ipfs/QmSXq2rPYs7Ec9FbpNp1k96apsApBFkZkcXgvCuKQQUcCx",
    "NAZGUL": "https://gateway.pinata.cloud/ipfs/QmbjVQ7qbmT6o5R1oYgFQ8jQp9sM1T6cusbPwR3s3tFwsG",
    "SAURON": "https://gateway.pinata.cloud/ipfs/QmYKPuTzFPvnK6t4VM1v1RDPiGRmEuQGVy1jmcsnHfws7x",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        ring_owner = get_ring_owner(advanced_collectible.tokenIdToRingOwner(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting TokenURI of {token_id}")
            set_tokenURI(
                token_id, advanced_collectible, ring_owner_metadata_dic[ring_owner]
            )


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
