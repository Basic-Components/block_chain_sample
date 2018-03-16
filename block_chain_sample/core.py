#cython: language_level=3
import json
import hashlib
from time import time
from collections import namedtuple
from typing import List, Optional
import cython
if not cython.compiled:
    import warnings
    warnings.warn("deprecated", DeprecationWarning)

Transactions = namedtuple('transactions', 'sender recipient amount')


class Block:
    index: int
    timestamp: float
    transactions: List[Transactions]
    proof: int
    previous_hash: str

    def __init__(self, index: int,
                 timestamp: float,
                 transactions: List[Transactions],
                 proof: int,
                 previous_hash: str)->None:

        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": dict(self.transactions._asdict()),
            "proof": self.proof,
            "previous_hash": self.previous_hash,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def hash(self, hash_func=hashlib.sha256):
        return hash_func.sha256(self.to_json()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof: int, previous_hash: Optional[str]=None):
        # Creates a new Block and adds it to the chain
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.hash(self.chain[-1])
        )

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int)->int:
        """[summary]

        Args:
            sender (str): [description]
            recipient (str): [description]
            amount (int): [description]
        """
        new_trans = Transactions(
            sender=sender,
            recipient=recipient,
            amount=amount,
        )
        self.current_transactions.append(new_trans)
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block: Block):
        # Hashes a Block
        pass

    @property
    def last_block(self):
        return self.chain[-1]
