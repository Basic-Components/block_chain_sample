import asyncio
from uuid import uuid4
from functools import partial
from concurrent import futures
from sanic import Sanic
from sanic.response import json
from .block_chain import blockchain

app = Sanic("blcok-chain-sample")
node_identifier = str(uuid4()).replace('-', '')


@app.listener('before_server_start')
async def setup_(app, loop):
    executor = futures.ProcessPoolExecutor()
    app.db = loop.set_default_executor(executor)


@app.get("/mine")
async def mine(request):

    last_block = blockchain.last_block
    last_proof = last_block.proof
    loop = asyncio.get_event_loop()
    proof_of_work = partial(blockchain.proof_of_work, last_proof)
    proof = await loop.run_in_executor(None, proof_of_work)

    # 给工作量证明的节点提供奖励.
    # 发送者为 "0" 表明是新挖出的币
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block.index,
        'transactions': block.transactions,
        'proof': block.proof,
        'previous_hash': block.previous_hash
    }
    return json(response)


@app.post('/transactions/new')
def new_transaction(request):
    """创建一次交易."""
    values = request.json

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values.keys() for k in required):
        return json({"message": 'Missing values'}, 400)

    # Create a new Transaction
    index = blockchain.new_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )

    response = {'message': f'Transaction will be added to Block {index}'}
    return json(response, 201)


@app.get('/chain')
def full_chain(request):
    """查看区块链的信息."""
    response = {
        'chain': [i._asdict() for i in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return json(response)


@app.post('/nodes/register')
def register_nodes(request):
    values = request.json

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return json(response, 201)


@app.get('/nodes/resolve')
def consensus(request):
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': [i._asdict() for i in blockchain.chain]
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': [i._asdict() for i in blockchain.chain]
        }

    return json(response)
