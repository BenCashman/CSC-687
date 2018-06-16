from json import dumps, loads
from time import time

from src.block import Block
from src.blockchain import Blockchain

'''
This class implements the necessary function for maintaining a blockchain, validating blocks, and generally
handling the details of the endpoints specified by a node in the TrustNet.
'''

class Server:
    def __init__(self, nodes):
        self.transactions = {}
        self.blockchain = Blockchain(nodes)
        
    def lastBlock(self):
        return self.blockchain.lastBlock
    
    def readAllBlocks(self, nodes):
        blocks = self.blockchain.getChain()
        return dumps(blocks), 200

    def updateWithNewBlock(self, request):
        data = loads(request.json())
        block = Block(data['index'], data['transactions'], data['timestamp'], data['previousHash'])
        proof = data['hash']
        newBlock = self.blockchain.addBlock(block, proof)
        if not newBlock:
            return 'block discarded by node', 409
        return 'block added to chain', 202

    def readSingleBlock(self, index):
        block = self.blockchain.getBlock(index)
        return dumps(block), 200

    def createNewBlock(self):
        if not self.transactions:
            return 'no pending transactions', 404
        newBlock = Block(self.blockchain.lastBlock.index + 1, self.transactions, time(), self.blockchain.lastBlock.currentHash)
        proof = self.blockchain.proofOfWork(newBlock)
        self.blockchain.addBlock(newBlock, proof)
        self.transactions = {}
        return 'new block created and added to chain', 201

    def createNewTransaction(self, data):
        requireds = [ 'id', 'request', 'sourceid', 'targetid']
        for required in requireds:
            if not data.get(required):
                return 'invalid transaction; missing {}'.format(required), 400
        if data['id'] in self.transactions:
            return 'ok', 200
        self.transactions[data['id']] = data
        print('Server.createNewTransacton() added new transaction')
        return 'ok', 201
    
    # ==============================================================================
    # debugging endpoints for prototype use
    # ==============================================================================
    def getTransactions(self):
        return "/transaction:getTransactions(" + dumps(self.transactions) + ")", 200
