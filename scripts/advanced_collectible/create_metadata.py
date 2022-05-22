from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_ring_owner, get_ring_owner_extension
from scripts.advanced_collectible.upload_to_pinata import upload_to_pinata
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests, json, os

ring_owner_to_image_uri = {
    "GANDALF": "https://ipfs.io/ipfs/QmafnxHphBY1tKPx6Z5njJaX64MFcHckX2RnpMdBLhPv2v?filename=gandalf.jpg",
    "NAZGUL": "https://ipfs.io/ipfs/QmYVSpFJtizu8tDXX7t4ZN7x2u4EyEV8QDHKhPxd1dDUo4?filename=nazgul.png",
    "SAURON": "https://ipfs.io/ipfs/Qmem1feA7masxGgD5zAu2XTXtQBKGgdpbQFx43NWJR9SwC?filename=sauron.jpeg",
}

ring_owner_to_image_uri_pinata = {
    "GANDALF": "https://gateway.pinata.cloud/ipfs/QmafnxHphBY1tKPx6Z5njJaX64MFcHckX2RnpMdBLhPv2v",
    "NAZGUL": "https://gateway.pinata.cloud/ipfs/QmYVSpFJtizu8tDXX7t4ZN7x2u4EyEV8QDHKhPxd1dDUo4",
    "SAURON": "https://gateway.pinata.cloud/ipfs/Qmem1feA7masxGgD5zAu2XTXtQBKGgdpbQFx43NWJR9SwC",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        ring_owner = get_ring_owner(advanced_collectible.tokenIdToRingOwner(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{ring_owner}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = ring_owner
            collectible_metadata[
                "description"
            ] = f"A fierce {ring_owner} from The Lord Of The Rings!"
            extension = get_ring_owner_extension(ring_owner).lower()
            print(extension)
            image_path = "./img/" + ring_owner.lower() + "." + extension

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
                image_pinata_uri = upload_to_pinata(image_path)
            image_uri = image_uri if image_uri else ring_owner_to_image_uri[ring_owner]

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)
                upload_to_pinata(metadata_file_name)


# curl -X POST -F file=@metadata/rinkeby/0-NAZGUL.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # Download stuff
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
