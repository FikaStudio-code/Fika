import json
import hashlib
import binascii
import threading
from copy import deepcopy
from .block import *

STOP_MINING = False
MINING_NOW = False
DIFFICULTY = 5

class PoW:
    def __init__(self, name):
        self.name = name
        self.chain = []
        self.chain_for_update = []
        self.previous_hash_for_update = ""
        self.lock = threading.Lock()

    def chained(self, block):
        with self.lock:
            self.chain.append(block)
        with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
            f.write("\nBlockchain is...\n{0}".format(json.dumps(self.chain, indent = 4)))

    def get_time(self):
        return self.chain[-1]["timestamp"]

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
        with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
            f.write("\nprevious_hash is {0}".format(bblock_hash))
        return bblock_hash

    def verify_block(self, previous_hash, block):
        global DIFFICULTY
        prefix = "0" * DIFFICULTY
        bblock = deepcopy(block)
        nonce = str(bblock["nonce"])
        del bblock["nonce"]
        text = json.dumps(bblock, sort_keys = True)

        item = (text + nonce).encode()
        digest = binascii.hexlify(self.double_hash(item)).decode("ascii")
        if digest.startswith(prefix):
            if previous_hash != bblock["previous_hash"]:
                if block["height"] > self.get_length():
                    with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
                        f.write("Invalid previous_hash! But this block may be orphan")
                    return (False, 1)
                else:
                    return (False, 0)
            else:
                with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
                    f.write("OK, valid block")
                return (True, 0)
        else:
            with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
                f.write("Error, invalid block(invalid 'nonce')")
            return (False, 0)

    def verify_chain(self, chain):
        if len(self.chain) >= len(chain):
            with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
                f.write("Received chain is shorter than mine.")
            return False
        else:
            result = self.renew_chain(chain)
            if result:
                return True
            else:
                return False

    def renew_chain(self, chain):
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
        with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
            f.write("\n\n!!!Blockchain update!!!{0}\n\n".format(json.dumps(self.chain, indent = 4)))
        return True

    def get_hash_for_update(self):
        bblock = deepcopy(self.chain_for_update[-1])
        bblock = json.dumps(bblock, sort_keys = True)
        bblock_hash = binascii.hexlify(self.double_hash(bblock.encode())).decode("ascii")
        self.previous_hash_for_update = bblock_hash

    def compute_nonce(self, block):
        global STOP_MINING
        global MINING_NOW
        global DIFFICULTY
        i = 0
        prefix = "0" * DIFFICULTY
        while STOP_MINING is False:
            nonce = str(i)
            item = (block + nonce).encode()
            result = binascii.hexlify(self.double_hash(item)).decode("ascii")
            if result.startswith(prefix):
                return nonce
            i += 1
        STOP_MINING = False
        MINING_NOW = False
        return False

    def mine_gblock(self):
        # Mining a GenesisBlock
        gblock = GenesisBlock().packing()
        self.chained(gblock)
        return self.get_hash(gblock)

    def mine_block(self, length, previous_hash):
        # Mining a Block
        block = Block(length, previous_hash, self.name).packing()
        nonce = self.compute_nonce(json.dumps(block, sort_keys = True))
        if nonce is not False:
            block["nonce"] = nonce
            return block
        else:
            return False

    def start_mining(self, previous_hash):
        global MINING_NOW
        MINING_NOW = True
        with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
            f.write("\nMining start!!!")
        length = self.get_length() + 1
        block = self.mine_block(length, previous_hash)
        if block is not False:
            if (block["previous_hash"] != self.get_hash(self.get_lastblock())) or (block["height"] != self.get_length() + 1):
                with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
                    f.write("\nOops! I might have lost mining competition")
                return 1, ""
            self.chained(block)
            previous_hash = self.get_hash(block)
            return 0, block
        return 1, ""


    def stop_mining(self):
        global STOP_MINING
        global MINING_NOW
        if MINING_NOW is True:
            STOP_MINING = True
