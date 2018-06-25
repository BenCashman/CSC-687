import datetime
import json

import requests
from flask import Flask, render_template, redirect, request

app = Flask(__name__)




CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8001"

posts = []

# fetchs data from the node's /chain endpoint, and parses and stores locally

def fetch_posts():
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain ["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["blockHash"] = block["previousHash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'], reverse=True)


# Creating the HTML to take user input and make a POST request to a connected node
# to add the transaction


@app.route('/')
def index():
    fetch_posts()
    return render_template('index.html',
            title='BlockScripts', posts=posts, node_address=CONNECTED_NODE_ADDRESS,
            readable_time=timestamp_to_string )
#transactionData = request.get_json()
# requiredFields = [ 'request', 'sourceid', 'targetid' ] note for postContent
@app.route('/submit', methods=['POST'])
def submitTextArea():

    postRequest = request.form['request']
    postSourceId = request.form['sourceid']
    postTargetId = request.form['targetid']
    grades = request.form['grades']



    postObject = {
        'grades' : grades,
        'request' : postRequest,
        'sourceid' : postSourceId,
        'targetid' : postTargetId
        }

# submit the transcation

    newTxAddress = "{}/transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(newTxAddress, json=postObject,
                headers={'Content-type': 'application/json'})

    return redirect('/')

def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
