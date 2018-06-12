from json import dumps
from src.block import Block
from src.validator import Validator
from time import time

'''
This class represents the abstraction of a Blockchain; that is, it maintains a list of valid blocks that
can be grown by adding new blocks.
'''

class Blockchain:
    def __init__(self):
        self.transactions = []
        self.chain = []
        self._createGenesisBlock()
    
    # ==========================================================================
    # public interface
    # ==========================================================================
    def addBlock(self, block, proof):
        previous = self.lastBlock.currentHash
        if previous != block.previousHash:
            return False
        if not Validator.isValidProof(block, proof):
            return False
        block.currentHash = proof
        self.chain.append(block)
        return True
     
    def getBlock(self, index):
        if index > 0 and index <= self.lastBlock.index:
            return dumps(self.chain[index].__dict__), 200
        else:
            return 'invalid index {}'.format(index), 400
       
    def getChain(self, nodes):
        Validator.checkChainValidity(self.chain)
        Validator.consensus(nodes, self.chain)
        data = []
        for block in self.chain:
            if not block.sequence == 0:  # do not include genesis block
                data.append(block.__dict__)
        return dumps({ 'length' : len(data), 'chain' : data })
    
    @property
    def lastBlock(self):
        return self.chain[-1]
     
    # ==========================================================================
    # private methods
    # ==========================================================================
    def _createGenesisBlock(self):
        block = Block(0, [], time(), '0')
        self.chain.append(block)
