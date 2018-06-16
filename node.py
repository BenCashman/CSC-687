from flask import Flask, request
from hashlib import sha256
from json import dumps, loads
from requests import get, post
from socket import gethostbyname, gethostname
from sys import argv

from src.server import Server
#from src.validator import Validator

'''
This code represents the public facing interface for a TrustNet network node.  It uses a Server object
to implement the internal function, simply passing data from the endpoints to that instance.  Additional
action that needs to take place between nodes on the TrustNet are dealt with here.  Further, it
initializes the Flask application, defines its endpoints, and starts it running.

To run the TrustNet network:
    To start the first node, type in:
        python3 node.py 8001
        
    To start subsequent nodes, type in:
        python3 node.py 800x <hostname> <port>
        
        where <hostname> is the previous node's host, and <port> is its port
        
    Each time a node is added, output from each running node indicates that a new node has joined TrustNet
    
HTTP response codes:  
  
    200           request handled OK
    201           entity created
    400           bad request, invalid parameters, etc.
'''

users = {}
nodes = set()

if len(argv) > 1:
    port = int(argv[1])
else:
    port = 8001
local = gethostbyname(gethostname()) + ':' + str(port)
  
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
        post(url, json=body, headers={ 'Content-type':'application/json' })
        response = get(url)
        addresses = loads(response.text)
        for address in addresses:
            unreached.add(address)
        nodes.add(node)
        reached.add(node)
    nodes.update(reached)
    
server = Server(nodes)

# ==============================================================================
# ReSTful endpoints specific to server, following CRUD terminology and usage
# ==============================================================================
app = Flask(__name__)

@app.route('/block', methods=['GET'])
def blockGET():
    return server.readAllBlocks(nodes)

@app.route('/block', methods=['POST'])
def blockPOST():
    return server.updateWithNewBlock(request)

@app.route('/block/<index>', methods=['GET'])
def blockIndexGET(index):
    return server.readSingleBlock(index)

@app.route('/mine', methods=['GET'])
def minePOST():
    return server.createNewBlock()

# ==============================================================================
# ReSTful endpoints specific to nodes, following CRUD terminology and usage
# ==============================================================================
@app.route('/node', methods=['GET'])
def nodeGET():
    return dumps(list(nodes)), 200

@app.route('/node', methods=['POST'])
def nodePOST():
    body = request.get_json()
    node = body['node']
    host, port = node.split(':')
    nodes.add(host + ':' + port)
    return 'OK', 200

@app.route('/transaction', methods=['POST'])
def transactionPOST():
    data = request.get_json()
    if not 'id' in data:
        data['id'] = sha256(dumps(data).encode()).hexdigest()
    message, rc = server.createNewTransaction(data)
    if rc == 201:
        for node in nodes:
            h, p = node.split(':')
            if h in local:
                url = 'http://localhost:' + p + '/transaction'
            else:
                url = 'http://{}/transaction'.format(node)
            post(url, json=data, headers={ 'Content-type':'application/json' })
    return message, rc

# ==============================================================================
# debugging endpoints for prototype use
# ==============================================================================
# endpoint to dump users
@app.route('/user', methods=['GET'])
def getUsers():
    return "/user:getUsers(" + dumps(users) + ")", 200

# endpoint to register a new user
@app.route('/user', methods=['POST'])
def addUser():
    body = request.get_json()
    handle = body['handle']
    ip = body['ip']
    uid = sha256((handle + ip).encode()).hexdigest()
    if uid in users.keys():
        return "id is not unique, try a new handle", 400
    users[id] = body
    return "/user:addUser(" + id + ")", 201

# endpoint to query id of a user by its handle
@app.route('/user/<user>', methods=['GET'])
def getUserIdByHandle(user):
    for uid in users.keys():
        if users[id]['handle'] == user:
            return uid, 200
    return "user " + user + " not registered", 400

# endpoint to dump transactions
@app.route('/transaction', methods=['GET'])
def transactionGET():
    return server.getTransactions()

# run Flask application
app.run(port=port, debug=True)
