import binascii
import hashlib
from copy import deepcopy
import json

def verify_block(previous_hash, block, difficulty = 4):
    prefix = "0" * difficulty
    bblock = deepcopy(block)
    nonce = str(bblock["nonce"])
    del bblock["nonce"]
    text = json.dumps(bblock, sort_keys = True)

    item = (text + nonce).encode()
    digest = binascii.hexlify(double_hash(item)).decode("ascii")
    if digest.startswith(prefix):
        if previous_hash != bblock["previous_hash"]:
            print("Invalid previous_hash! But this block may be orphan")
            return (False, 1)
        else:
            print("OK, valid block")
            return (True, 0)
    else:
        print("Error, invalid block(invalid 'nonce')")
        return (False, 0)

def double_hash(item):
    return hashlib.sha256(hashlib.sha256(item).digest()).digest()

def get_hash(block):
    bblock = deepcopy(block)
    bblock = json.dumps(bblock, sort_keys = True)
    bblock_hash = binascii.hexlify(double_hash(bblock.encode())).decode("ascii")
    print("previous_hash is {0}".format(bblock_hash))
    return bblock_hash

def main():
    blockchain = [
        {
            "height": 1,
            "nonce": 0,
            "previous_hash": "This is genesis block!",
            "timestamp": 0
        },
        {
            "height": 2,
            "nonce": "13636",
            "previous_hash": "e4a9e6d1bee0344151641e86058c33841978a7286f55fbd688c1c3f195088d19",
            "timestamp": 1568704842.2840068
        },
        {
            "height": 3,
            "nonce": "30470",
            "previous_hash": "a32ec226ab52906a83f56d366e5f9e04ce32713082be2d90d1fddfec65a0bd33",
            "timestamp": 1568704852.3671236
        },
        {
            "height": 4,
            "nonce": "15322",
            "previous_hash": "4c54d15b7460b089a03ae34ce5c0ed10ff62d6613ec9cbe729458236cf4e5cb9",
            "timestamp": 1568704852.5556006
        },
        {
            "height": 5,
            "nonce": "120531",
            "previous_hash": "e32aec52bb1b337b570d0858113ebe24cb4213eb7b4ba4fa8cd1814c31cb5c1a",
            "timestamp": 1568704862.7125397
        },
        {
            "height": 6,
            "nonce": "7779",
            "previous_hash": "47e6ac6ca05dc907444eeda8f9d703d3b0101566c02bba3ef9778a5070837f22",
            "timestamp": 1568704874.5093713
        },
        {
            "height": 7,
            "nonce": "26067",
            "previous_hash": "584d722a81ccfdd61a41597f34cec87e0824967b5ed26a41de4f4dad8a772bbd",
            "timestamp": 1568704884.6751385
        },
        {
            "height": 8,
            "nonce": "11078",
            "previous_hash": "982c6748f3399e9f7318f93349254052e091132c1c800c2a790e374dded5411f",
            "timestamp": 1568704895.111833
        },
        {
            "height": 9,
            "nonce": "25260",
            "previous_hash": "5cecec980d2af5f490671ded3cf0e2b07a79dc3aa25c30a3ce5916470c729e30",
            "timestamp": 1568704980.1736748
        },
        {
            "height": 10,
            "nonce": "62078",
            "previous_hash": "bacb027d3c74bb8f6f07929c8d1c87159846cf7badb33fc4fab5c04ce2dc24d7",
            "timestamp": 1568705065.2989743
        },
        {
            "height": 11,
            "nonce": "53715",
            "previous_hash": "e3be7642aabfd1943ee522069a1e816b05033e0ab3992cc621e83d50f7d33177",
            "timestamp": 1568705088.2296813
        },
        {
            "height": 12,
            "nonce": "50349",
            "previous_hash": "64cc4d84907d8dd043fb5ab37e74766a789e862cb2b6ee09a66abfef30ceaf4b",
            "timestamp": 1568705111.1066706
        },
        {
            "height": 13,
            "nonce": "1454",
            "previous_hash": "71d3c14300cca1a8393510705fb243f1470bfe7e2ff675b51594558472d4c910",
            "timestamp": 1568705133.9702337
        }
    ]

    previous_hash = "e4a9e6d1bee0344151641e86058c33841978a7286f55fbd688c1c3f195088d19"
    for block in blockchain:
        if block["height"] != 1:
            result, hoge = verify_block(previous_hash, block)
            previous_hash = get_hash(block)

if __name__ == "__main__":
    main()
