from unittest import TestCase
from src.block import Block
 
class TestBlock(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def testInstantiationNoIndex(self):
        self.assertRaises(TypeError, lambda: Block(transactions = [], timestamp = 0, previousHash = 0))
        
    def testInstantiationNoTransactions(self):
        self.assertRaises(TypeError, lambda: Block(index = 0, timestamp = 0, previousHash = 0))  
        
    def testInstantiationNoTimestamp(self):
        self.assertRaises(TypeError, lambda: Block(index = 0, transactions = [], previousHash = 0))  
        
    def testInstantiationNoPreviousHash(self):
        self.assertRaises(TypeError, lambda: Block(index = 0, transactions = [], timestamp = 0))    
    
    def testInstanatiationGenesisBlock(self):
        b = Block(0, [], 0, 0)
        self.assertEqual(b.previousHash, 0)
        
    def testInstantiationBasicBlock(self):
        index = 123
        transactions = [ 1, 2, 3 ]
        timestamp = 999388
        hashvalue = 123456
        
        b = Block(index, transactions, timestamp, hashvalue)
        self.assertEqual(b.index, index)
        self.assertEqual(b.transactions, transactions)
        self.assertEqual(b.timestamp, timestamp)
        self.assertEqual(b.previousHash, hashvalue)
        