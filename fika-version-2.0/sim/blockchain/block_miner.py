from .block import *

class BlockMiner:
    def __init__(self):
        pass

    def mine_block(self, length, previous_hash):
        # Mining a Block
        block = Block(length, previous_hash)
        return block.packing()

    def mine_gblock(self):
        # Mining a GenesisBlock
        gblock = GenesisBlock()
        return gblock.packing()
