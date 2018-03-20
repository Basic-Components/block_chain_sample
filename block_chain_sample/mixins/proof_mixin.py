import hashlib


class ProofMixin:
    """实现工作量证明"""

    def proof_of_work(self, last_proof):
        """寻找工作量证明.

        简单的工作量证明:
         - 查找一个 p' 使得 hash(pp') 以4个0开头
         - p 是上一个块的证明,  p' 是当前的证明

        Args:
            last_proof (int): 上一次的工作量证明

        Returns:
            (int): 计算出的工作量证明

        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """验证工作量证明.

        是否hash(last_proof, proof)以4个0开头?
        Args:
            last_proof (int): 上一次的工作量证明
            proof (int): 要验证的工作量证明

        Returns:
            (bool): 检验出来的结果

        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
