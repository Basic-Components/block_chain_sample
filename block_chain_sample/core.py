import json
import hashlib
from time import time
from collections import namedtuple, OrderedDict
from typing import Optional
from .mixins.hash_mixin import HashMixin



class Transactions(namedtuple('transactions', 'sender recipient amount'), HashMixin):
    """记录一次交易行为.

    Attributes:
        sender (str): 发送方地址
        recipient (str): 接收方地址
        amount (int): 交易金额

    """

    def _asdict(self):
        org_dict = super()._asdict()
        return dict(org_dict)


class Block(namedtuple('block', 'index timestamp transactions proof previous_hash'), HashMixin):
    """[summary]

    Attributes:
        index (int): 区块的长度
        timestamp (int): 区块生成的时间戳
        transactions (List[Transactions]): 区块包含的交易
        proof (int): 工作量证明
        previous_hash (str): 上一区块的hash

    """

    def _asdict(self):
        org_dict = super()._asdict()
        return {
            i: ([j._asdict() for j in v] if i == 'transactions' else v)
            for i, v in org_dict.items()
        }

    def hash(self, hash_func=hashlib.sha256):
        org_dict = {
            i: ([j.hash() for j in v] if i == 'transactions' else v)
            for i, v in super()._asdict().items()
        }
        return hash_func(json.dumps(org_dict, sort_keys=True).encode("utf-8")).hexdigest()


class Core:
    """区块链类."""

    @property
    def last_block(self):
        return self.chain[-1]

    def __init__(self):
        """初始化一个区块链.

        Attributes:
            chain (List[Block]): - 区块链容器
            current_transactions (Transactions): - 最近的一次交易

        Property:
            last_block (Blcok): - 链中最后一块区块

        """
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof: int, previous_hash: Optional[str] = None):
        """创建一个区块.

        Args:
            proof (int): 校验
            previous_hash (Optional[str], optional): Defaults to None. 上一块区块的hash

        Returns:
            (Block): 返回创建出的区块对象

        """
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.chain[-1].hash()
        )

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int)->int:
        """新增一条交易记录.

        Args:
            sender (str): 发送者
            recipient (str): 接收者
            amount (int): 交易金额

        """
        new_trans = Transactions(
            sender=sender,
            recipient=recipient,
            amount=amount,
        )
        self.current_transactions.append(new_trans)
        return self.last_block.index + 1

