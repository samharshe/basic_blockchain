import hashlib

genesis_message = ""
usernames = []
balances = []
ledger = {}
blocks = []

def set_num_users():
    while True:
        try:
            global num_users
            num_users = int(raw_input("How many users are there on the network? "))
            if num_users > 0:
                break
            else:
                print("Please enter a natural number.")
        except(ValueError, NameError, SyntaxError):
            print("Please enter a natural number.")
            continue

def set_usernames():
    for i in range(num_users):
        username_input_ok = False
        while(not username_input_ok):
            username_duplicate = False
            username_input = raw_input("What is the name of user #" + str(i+1) + " in this network? ")
            for username in usernames:
                if username == username_input:
                    username_duplicate = True
                    print("Please enter a unique username for user #" + str(i+1))

            if not username_duplicate:
                usernames.append(username_input)
                username_input_ok = True

def set_user_balances():
    for i in range(num_users):
        while True:
            try:
                balance_input = float(raw_input("What is the initial balance of " + usernames[i] + "? "))
                if balance_input > 0:
                    balances.append(balance_input)
                    break
                else:
                    print("Please enter a positive number.")
            except(ValueError, NameError, SyntaxError):
                print("Please enter a positive number.")
                continue

def set_ledger():
    for i in range(num_users):
        ledger[usernames[i]] = balances[i]

def set_genesis_message():
    genesis_message = raw_input("What would you like the message of the Genesis block to be? ")

def initialize():
    print('\n')
    set_num_users()
    print('\n')
    set_usernames()
    print('\n')
    set_user_balances()
    print('\n')
    set_ledger()
    print_ledger()
    set_genesis_message()
    print('\n')

class Block():
    def __init__(self, block_index, previous_hash, ledger, transactions):
        self.block_index = block_index
        self.previous_hash = previous_hash
        self.ledger = ledger
        self.transactions = transactions
        self.hash_input = "{}{}{}{}".format(block_index, previous_hash, ledger, transactions)
        self.hash = hashlib.sha256(self.hash_input.encode()).hexdigest()

    def print_block_summary(self):
        print("BLOCK #{}".format(self.block_index))
        print("Previous block hash: {}".format(self.previous_hash))
        print("Transactions:")
        for transaction in self.transactions:
            print('\t{}'.format(transaction))
        print("Hash: {}\n".format(self.hash))

    def get_hash(self):
        return self.hash

def get_sending_user():
    while True:
            try:
                sending_user = raw_input("What is the username of the sender of this transaction? ")
                if ledger[sending_user] == 0:
                    print("Please choose a user with a balance greater than $0.\n")
                elif sending_user not in ledger.keys():
                    print("Please enter the username of an existing user.")
                else:
                    return sending_user
            except(ValueError, NameError, SyntaxError):
                continue

def get_receiving_user(sending_user):
    while True:
                try:
                    receiving_user = raw_input("What is the username of the recipient of this transaction? ")
                    if receiving_user in ledger.keys() and receiving_user != sending_user:
                        return receiving_user
                    else:
                        print("Please enter a valid recipient of the transaction.")
                except(ValueError, NameError, SyntaxError):
                    continue

def get_amount(sending_user, receiving_user):
    while True:
        try:
            amount = float(raw_input(sending_user + " has a current balance of $" + str(ledger[sending_user]) + ". How much would you like " + sending_user + " to send to " + receiving_user + "? "))
            print('\n')
            if amount >= 0 and amount <= ledger[sending_user]:
                ledger[sending_user] -= amount
                ledger[receiving_user] += amount
                return "${} from {} to {}".format(amount, sending_user, receiving_user)
            else:
                print("Please choose a number between zero and " + sending_user + "\'s account balance of " + str(ledger[sending_user]))
        except(ValueError, NameError, SyntaxError):
            continue

def print_transactions(transactions):
    print("The current transactions to be included on this block:")
    for i in range(len(transactions)):
        print("\t {}. {}".format(i + 1, transactions[i]))
    print('\n')

def check_submit_block():
    while True:
        try:
            submit_input = raw_input("Press enter to submit this block. Press any other button and then enter to add additional transactions.")
            print('\n')
            if(len(submit_input) == 0):
                submit_block = True
            else:
                submit_block = False
            return submit_block
        except(ValueError, NameError, SyntaxError):
            continue

def create_block():
    print("Create transactions to add to block " + str(len(blocks)) + ".\n")
    transactions = []
    submit_block = False
    while not submit_block:
        print_ledger()
        sending_user = get_sending_user()
        receiving_user = get_receiving_user(sending_user)
        transactions.append(get_amount(sending_user, receiving_user))
        print_transactions(transactions)
        print_ledger()
        submit_block = check_submit_block()

    blocks.append(Block(len(blocks), blocks[len(blocks) - 1].get_hash(), ledger, transactions))
    blocks[-1].print_block_summary()

def print_ledger():
    print("Current ledger:")
    for i in range(len(ledger)):
        print("\t{}: ${}".format(ledger.keys()[i], ledger.values()[i]))
    print('\n')

def main():
    initialize()
    blocks.append(Block(0, genesis_message, ledger, []))
    while True:
        if raw_input("Press \"n\" then ENTER to terminate this program. Press anything else then ENTER to continue.").upper() == "N":
            break
        print('\n')
        create_block() 

main()