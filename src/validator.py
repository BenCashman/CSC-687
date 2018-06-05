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
    def isValidProof(block, proof, difficulty):
        return proof.startswith('0' * difficulty ) and proof == block.computeHash()
    
    @staticmethod
    def checkChainValidity(chain):  # todo implement
        pass

    @staticmethod
    def consensus(chain):  # todo implement
        pass
    