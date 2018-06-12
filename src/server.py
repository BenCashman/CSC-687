from json import dumps, loads
from time import time

from src.block import Block
from src.blockchain import Blockchain
from src.validator import Validator

'''
This class implements the necessary function for maintaining a blockchain, validating blocks, and generally
handling the details of the endpoints specified by a node in the TrustNet.
'''

class Server:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.transactions = {}
        self.blockchain = Blockchain()
    
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
            return False
        lastBlock = self.lastBlock
        newBlock = Block(index=lastBlock.index + 1, transactions=self.transactions, timestamp=time.timestamp(), previousHash = lastBlock.hash)
        proof = Validator.proofOfWork(newBlock, self.difficulty)
        self.blockchain.addBlock(newBlock, proof)
        self.transactions = {}
        return newBlock.index

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
