'''
This class represents algorithms that satisfy particular verification criteria.  As a separate class it
allows a pluggable interface so that different subclass implementations of these algorithms can be used
as the need for them may arise.
'''

class Validator:  # todo needs testcases and implementation
    @staticmethod
    def proofOfWord(block):  # todo implement
        pass
    
    @staticmethod
    def isValidProof(block, proof):  # todo implement
        pass
    
    @staticmethod
    def checkChainValidity(chain):  # todo implement
        pass

    @staticmethod
    def consensus(chain):  # todo implement
        pass
    