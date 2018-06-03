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

'''
hints:
    req = request.get_json()
    rc = 200
    if req['node'] not in nodes:
        nodes.add(req['node'])
        rc = 201
    return dumps(list(nodes)) + '\n', rc
'''
