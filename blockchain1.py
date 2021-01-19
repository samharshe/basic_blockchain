import time
import hashlib

class Transaction(object): 
    def __init__(self, sending_indices, receiving_indices, amounts, ledger):
        self.sending_indices = sending_indices
        self.receiving_indices = receiving_indices
        self.amounts = amounts
        self.new_ledger = ledger
        self.update_ledger()
    
    def update_ledger(self):
        bad_transaction = False
        if(len(self.sending_indices) == len(self.receiving_indices) == len(self.amounts)):
            print("LENGTHS OK!")
            for i in range(len(self.sending_indices)):
                self.new_ledger[self.sending_indices[i]-1] -= self.amounts[i]
                self.new_ledger[self.receiving_indices[i]-1] += self.amounts[i]
            for amount in self.new_ledger:
                if amount < 0:
                    bad_transaction = True
        else:
            print("LENGTHS NOT OK!")



        if(bad_transaction):
            print(self.ledger)
            return self.ledger
        else:
            print(self.new_ledger)
            return self.new_ledger

class Block(object):

    def __init__(self, index, previous_hash, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions

    def get_block_hash(self):
        self.hash_input = "{}{}{}".format(self.index, self.previous_hash, self.transactions)
        return hashlib.sha256(self.hash_input.encode()).hexdigest()

    def __repr__(self):
        return "block index: {} | previous hash: {} | transactions: {}".format(self.index, self.previous_hash, self.transactions)


