import json
import hashlib
import binascii
import threading
from copy import deepcopy

class BlockchainManager:
    def __init__(self):
        self.chain = []
        self.chain_for_update = []
        self.previous_hash_for_update = ""
        self.lock = threading.Lock()

    def chained(self, block):
        with self.lock:
            self.chain.append(block)
        with open("/fika/output/log.txt", "a") as f:
            f.write("\nBlockchain is...\n{0}".format(json.dumps(self.chain, indent = 4)))

    def get_length(self):
        return len(self.chain)

    def get_mychain(self):
        return self.chain

    def get_lastblock(self):
        return self.chain[-1]

    def double_hash(slef, item):
        return hashlib.sha256(hashlib.sha256(item).digest()).digest()

    def get_hash(self, block):
        bblock = deepcopy(block)
        bblock = json.dumps(bblock, sort_keys = True)
        bblock_hash = binascii.hexlify(self.double_hash(bblock.encode())).decode("ascii")
        with open("/fika/output/log.txt", "a") as f:
            f.write("\nprevious_hash is {0}".format(bblock_hash))
        return bblock_hash

    def verify_block(self, previous_hash, block, difficulty = 4):
        prefix = "0" * difficulty
        bblock = deepcopy(block)
        nonce = str(bblock["nonce"])
        del bblock["nonce"]
        text = json.dumps(bblock, sort_keys = True)

        item = (text + nonce).encode()
        digest = binascii.hexlify(self.double_hash(item)).decode("ascii")
        if digest.startswith(prefix):
            if previous_hash != bblock["previous_hash"]:
                with open("/fika/output/log.txt", "a") as f:
                    f.write("Invalid previous_hash! But this block may be orphan")
                return (False, 1)
            else:
                with open("/fika/output/log.txt", "a") as f:
                    f.write("OK, valid block")
                return (True, 0)
        else:
            with open("/fika/output/log.txt", "a") as f:
                f.write("Error, invalid block(invalid 'nonce')")
            return (False, 0)

    def verify_chain(self, chain):
        if len(self.chain) >= len(chain):
            with open("/fika/output/log.txt", "a") as f:
                f.write("Received chain is shorter than mine.")
            return False
        else:
            result = self.renew_chain(chain)
            if result:
                return True
            else:
                return False

    def renew_chain(self, chain, difficulty = 4):
        # This method need improvementation
        # if it wants renew chain, renew_chain need only orphan block
        # but now, this method receive full chain
        self.chain_for_update = []
        self.previous_hash_for_update = ""
        for block in chain:
            if block["height"] > 1:
                result, hoge = self.verify_block(self.previous_hash_for_update, block)
                if result:
                    self.chain_for_update.append(block)
                    self.get_hash_for_update()
                else:
                    return False
            else:
                self.chain_for_update.append(block)
                self.get_hash_for_update()
        self.chain = deepcopy(self.chain_for_update)
        with open("/fika/output/log.txt", "a") as f:
            f.write("\n\n!!!Blockchain update!!!{0}\n\n".format(json.dumps(self.chain, indent = 4)))
        return True

    def get_hash_for_update(self):
        bblock = deepcopy(self.chain_for_update[-1])
        bblock = json.dumps(bblock, sort_keys = True)
        bblock_hash = binascii.hexlify(self.double_hash(bblock.encode())).decode("ascii")
        self.previous_hash_for_update = bblock_hash
