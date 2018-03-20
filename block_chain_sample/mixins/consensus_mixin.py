import aiohttp


class ConsensusMixin:

    def valid_chain(self, chain):
        """检验链的有效性.
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block.previous_hash != last_block.hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    async def resolve_conflicts(self):
        """
        共识算法解决冲突
        使用网络中最长的链.
        :return: <bool> True 如果链被取代, 否则为False
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://{node}/chain') as resp:
                    if resp.status == 200:
                        resp_json = await resp.json()
                        length = resp_json['length']
                        chain = resp_json['chain']
                        # Check if the length is longer and the chain is valid
                        if length > max_length and self.valid_chain(chain):
                            max_length = length
                            new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False
