from time import time
import binascii
import hashlib
import json

class Block:
    def __init__(self, height, previous_hash):
        self.height = height
        self.timestamp = time()
        self.previous_hash = previous_hash

    def packing(self):
        block = {
            "height": self.height,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
        }
        nonce = self.compute_nonce(json.dumps(block, sort_keys = True))
        block["nonce"] = nonce
        return block

    def compute_nonce(self, block, difficulty = 4):
        i = 0
        prefix = "0" * difficulty
        while True:
            nonce = str(i)
            item = (block + nonce).encode()
            result = binascii.hexlify(self.double_hash(item)).decode("ascii")
            if result.startswith(prefix):
                return nonce
            i += 1

    def double_hash(self, item):
        return hashlib.sha256(hashlib.sha256(item).digest()).digest()

class GenesisBlock:
    def __init__(self):
        pass

    def packing(self):
        gblock = {
            "height": 1,
            "timestamp": 0,
            "nonce": 0,
            "previous_hash": "This is genesis block!",
        }
        return gblock
