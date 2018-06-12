'''
This class represents algorithms that satisfy particular verification criteria.  As a separate class it
allows a pluggable interface so that different subclass implementations of these algorithms can be used
as the need for them may arise.
'''

class Validator:
    @staticmethod
    def proofOfWork(block, difficulty):
        block.nonce = 0
        proof = block.computeHash()
        while not proof.startswith('0' * difficulty):
            block.nonce += 1
            proof = block.computeHash()
        return proof
    
    @staticmethod
    def _isValidProof(block, proof, difficulty):
        return proof.startswith('0' * difficulty ) and proof == block.computeHash()
    
    @staticmethod
    def checkChainValidity(chain, difficulty):
        result = True
        previous = '0'
        for block in chain:
            blockHash = block.hash
            delattr(block, 'hash')
            if not Validator.isValidProof(block, blockHash, difficulty) or previous != block.previousHash:
                result = False
                break
            block.hash, previous = blockHash, blockHash
        return result

    @staticmethod
    def consensus(nodes, chain):
        length = len(chain)
        # bugbug needs implementation
    