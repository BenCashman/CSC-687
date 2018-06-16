from hashlib import sha256
from json import dumps

'''
This class implements the abstraction of a block which is composed of a set of transactions, an index number,
a nonce, a previous hash, and the block's own hash called current hash.  The block is responsible for generating
its own hash value, not trusting any other entity to do so.
'''

class Block:
    def __init__(self, index, transactions, timestamp, previousHash):
        if index == None:
            raise ValueError('missing index value')
        if index < 0:
            raise ValueError('index is negative')
        self.index = index
        
        if transactions == None:
            raise ValueError('missing transactions')
        self.transactions = transactions
        
        if timestamp == None:
            raise ValueError('missing timestamp')
        self.timestamp = timestamp
                
        if previousHash == None:
            raise ValueError('missing previous hash')
        self.previousHash = previousHash
        
        self.nonce = 0
        self.currentHash = 0
        
    # ==========================================================================
    # public interface
    # ==========================================================================
    def computeHash(self):
        contents = dumps(self.__dict__, sort_keys=True)
        return sha256(contents.encode()).hexdigest()
    