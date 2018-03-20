from .core import Core
from .mixins.proof_mixin import ProofMixin
from .mixins.consensus_mixin import ConsensusMixin
from .mixins.regist_node_mixin import RegistNodeMixin


class Blockchain(Core, ProofMixin, RegistNodeMixin, ConsensusMixin):
    def __init__(self):
        super().__init__()
        RegistNodeMixin.__init__(self)


blockchain = Blockchain()

__all__ = ["blockchain"]
