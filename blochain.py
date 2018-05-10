import hashlib
from flask import Flask
from flask import request
import json
from datetime import datetime


app = Flask(__name__)


class Block:
    def __init__(self, index, timestamp, data, prev_hash):
            self.index = index
            self.timestamp = timestamp
            self.data = data
            self.prev_hash = prev_hash
            self.hash = self.hash_block()

    def hash_block(self):
            hashed = hashlib.sha3_256(str(self.index).encode() + str(self.timestamp).encode()
                                      + str(self.data).encode() + str(self.prev_hash).encode()).hexdigest()
            return hashed

def genesis_block():
    return Block(0, datetime.now(), "helloworld", 0)

def next_block(last_block):
    next_index = last_block.index + 1
    next_timestamp = datetime.now()
    next_data = "yabadabadoo" + str(next_index)
    next_hash = last_block.hash
    return Block(next_index, next_timestamp, next_data, next_hash)


blockchain = [genesis_block()]
prev_block = blockchain[0]

def proof_of_work(last_block):
    counter = last_block + 1

    while not (counter % 10 == 0 and counter % last_block == 0):
        counter+=1

    return counter


for i in range(0,20):
    new_block = next_block(prev_block)
    blockchain.append(new_block)
    prev_block = new_block

    print ("Block #{} has been added to the blockchain!".format(new_block.index))
    print ("Hash: {}\n".format(new_block.hash))

block_txns = []

@app.route('/txn', methods=['POST'])
def txn():
    if request.method == 'POST':
        new_txn = request.get_json()
        block_txns.append(new_txn)

        return "Transaction submitted"

miner_address = "home sweet home"

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[:-1]
    last_proof = last_block.data['proof-of-work']

    proof = proof_of_work(last_proof)

    block_txns.append({"from" : "network", "to" : miner_address, "amount" : 1})

    new_data = {"proof-of-work" : proof, "txn" : list[block_txns]}

    new_index = last_block.index + 1
    new_timestamp = datetime.now()
    new_hash = last_block.hash

    newBlock = Block(new_index, new_timestamp, new_data, new_hash)

    blockchain.append(newBlock)

    return json.dumps({
      "index": new_index,
      "timestamp": str(new_timestamp),
      "data": new_data,
      "hash": new_hash
  }) + "\n"




