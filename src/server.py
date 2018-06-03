from json import dumps

from src.blockchain import Blockchain

'''
This class implements the necessary function for maintaining a blockchain, validating blocks, and generally
handling the details of the endpoints specified by a node in the TrustNet.
'''

class Server:
    def __init__(self):
        self.transactions = {}
        self.blockchain = Blockchain()
    
    def readAllBlocks(self):  # todo implement
        pass

    def updateWithNewBlock(self, request):  # todo implement
        pass

    def readSingleBlock(self, index):  # todo implement
        block = self.blockchain.getBlock(index)
        return 
        pass

    def createNewBlock(self, request):  # todo implement
        pass

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
