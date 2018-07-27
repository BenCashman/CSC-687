from flask import Flask, request
from hashlib import sha256
from json import dumps, loads
from requests import get, post
from socket import gethostbyname, gethostname
from sys import argv
from time import time

if len(argv) > 1:
    port = int(argv[1])
else:
    port = 8001
local = gethostbyname(gethostname()) + ':' + str(port)

nodes = set()
if len(argv) > 3:
    if argv[2] == 'localhost':
        remote = gethostbyname(gethostname()) + ':' + argv[3]
    else:
        remote = argv[2] + ':' + argv[3]
        
    reached = set()
    unreached = set()
    unreached.add(remote)
    body = { 'node' : local }
    while len(unreached) > 0:
        node = unreached.pop()
        if node in reached or node == local:
            continue
        h, p = node.split(':')
        if h in local:
            url = 'http://localhost:' + p + '/node'
        else:
            url = 'http://{}/node'.format(node)
        post(url, json=body, headers={ 'content-type':'application/json' })
        response = get(url)
        addresses = loads(response.text)
        for address in addresses:
            unreached.add(address)
        nodes.add(node)
        reached.add(node)
    nodes.update(reached)

# ==============================================================================
# define Block class
# ==============================================================================
class Block:
    def __init__(self, index, transactions, timestamp, previousHash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.nonce = nonce

    def computeHash(self):
        timestamp = self.timestamp
        self.timestamp = 0
        data = dumps(self.__dict__, sort_keys=True)
        encoding = sha256(data.encode()).hexdigest()
        self.timestamp = timestamp
        return encoding

# ==============================================================================
# define BlockChain class
# ==============================================================================
class Blockchain:
    difficulty = 2

    def __init__(self):
        self.unconfirmedTransactions = []
        self.chain = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        genesisBlock = Block(0, [], time(), '0')
        genesisBlock.currentHash = genesisBlock.computeHash()
        self.chain.append(genesisBlock)

    @property
    def lastBlock(self):
        return self.chain[-1]
# FUnc to add new blocks to the chain, must connect to previous block
    def addBlock(self, block, proof):
        previousHash = self.lastBlock.currentHash
        if previousHash != block.previousHash:
            return False
        if not Blockchain.isValidProof(block, proof):
            return False
        block.currentHash = proof
        self.chain.append(block)
        return True
#Function to enable mining of blocks - note the nonce value
    def proofOfWork(self, block):
        block.nonce = 0
        computedHash = block.computeHash()
        while not computedHash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computedHash = block.computeHash()
        return computedHash

    def addNewTransaction(self, transaction):
        self.unconfirmedTransactions.append(transaction)
        
#func to determine if a minner's proof of work is valid
    @classmethod
    def isValidProof(cls, block, blockHash):
        lhs = blockHash.startswith('0' * Blockchain.difficulty)
        computedHash = block.computeHash()
        rhs = blockHash == computedHash
        return lhs and rhs

    @classmethod
    def checkChainValidity(cls, chain):
        previousHash = '0'
        for block in chain:
            blockHash = block.currentHash
            delattr(block, 'currentHash')
            timestamp = block.timestamp
            block.timestamp = 0
            if not cls.isValidProof(block, blockHash) or previousHash != block.previousHash:
                return False
            block.currentHash, previousHash, block.timestamp = blockHash, blockHash, timestamp
        return True

    def mine(self):
        if not self.unconfirmedTransactions:
            return False
        lastBlock = self.lastBlock
        newBlock = Block(index=lastBlock.index + 1, transactions=self.unconfirmedTransactions,
                timestamp=time(), previousHash=lastBlock.currentHash)
        proof = self.proofOfWork(newBlock)
        self.addBlock(newBlock, proof)
        self.unconfirmedTransactions = []
        announceNewBlock(newBlock)
        return newBlock.index
    
# ==============================================================================
# define global variables
# ==============================================================================   
app = Flask(__name__)
blockchain = Blockchain()

# ==============================================================================
# define global functions
# ==============================================================================
def getConsensus():
    global blockchain
    longestChain = None
    currentLength = len(blockchain.chain)
    for node in nodes:
        response = get('http://{}/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > currentLength and blockchain.checkChainValidity(chain):
            currentLength = length
            longestChain = chain
    if longestChain:
        blockchain = longestChain
        return True
    return False

def announceNewBlock(block):
    for node in nodes:
        h, p = node.split(':')
        if h in local:
            url = 'http://localhost:' + p + '/block'
        else:
            url = 'http://{}/block'.format(node)
        post(url, data=dumps(block.__dict__, sort_keys=True), headers={ 'Content-type':'application/json' })

# ==============================================================================
# ReSTful endpoints specific to nodes, following CRUD terminology and usage
# ==============================================================================
@app.route('/node', methods=['GET'])
def getAllNodes():
    return dumps(list(nodes)), 200

@app.route('/node', methods=['POST'])
def addNewNode():
    body = request.get_json()
    node = body['node']
    if not node in nodes:
        nodes.add(node)
        return 'OK', 201
    else:
        return 'node already added', 200

# ==============================================================================
# ReSTful endpoints specific to transactions, following CRUD terminology and usage
# ==============================================================================
@app.route('/transaction', methods=['GET'])
def getPendingTransactions():
    return dumps(blockchain.unconfirmedTransactions)

@app.route('/transaction', methods=['POST'])
def addNewTransaction():
    transactionData = request.get_json()
    requiredFields = [ 'request', 'sourceid', 'targetid' ]
    for field in requiredFields:
        if not transactionData.get(field):
            return 'transaction missing {} field'.format(field), 404
    transactionData['timestamp'] = time()
    blockchain.addNewTransaction(transactionData)
    return 'transaction added successfully ', 201

# ==============================================================================
# ReSTful endpoints specific to chains, following CRUD terminology and usage
# ==============================================================================
@app.route('/chain', methods=['GET'])
def getChain():
    getConsensus()
    chainData = []
    for block in blockchain.chain:
        chainData.append(block.__dict__)
    return dumps({ 'length': len(chainData), 'chain': chainData })

@app.route('/mine', methods=['GET'])
def mineTransactions():
    result = blockchain.mine()
    if not result:
        return 'No transactions to mine'
    return 'Block #{} is mined'.format(result), 201

@app.route('/block', methods=['POST'])
def validateAndAddBlock():
    blockData = request.get_json()
    block = Block(blockData['index'], blockData['transactions'], blockData['timestamp'], blockData['previousHash'], blockData['nonce'])
    proof = blockData['currentHash']
    added = blockchain.addBlock(block, proof)
    if not added:
        return 'The block was discarded by the node', 400
    return 'Block added to the chain', 201

# run Flask application
app.run(port=port, debug=False)
