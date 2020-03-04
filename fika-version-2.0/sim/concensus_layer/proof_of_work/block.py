from time import time

class Block:
    def __init__(self, height, previous_hash, miner):
        self.height = height
        self.time = time()
        self.previous_hash = previous_hash
        self.miner = miner

    def packing(self):
        block = {
            "height": self.height,
            "timestamp": self.time,
            "miner": self.miner,
            "previous_hash": self.previous_hash,
        }
        return block

"""
    def packing(self):
        block = {
            "height": self.height,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
        }


    def compute_nonce(self, block, difficulty = 5):
        global STOP_MINING
        i = 0
        prefix = "0" * difficulty
        while STOP_MINING is False:
            nonce = str(i)
            item = (block + nonce).encode()
            result = binascii.hexlify(self.double_hash(item)).decode("ascii")
            if result.startswith(prefix):
                return nonce
            i += 1

    def double_hash(self, item):
        return hashlib.sha256(hashlib.sha256(item).digest()).digest()
"""

class GenesisBlock:
    def __init__(self):
        pass

    def packing(self):
        gblock = {
            "height": 1,
            "timestamp": 0,
            "nonce": 0,
            "miner": "No One",
            "previous_hash": "This is genesis block!",
        }
        return gblock
