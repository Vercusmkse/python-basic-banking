import uuid


class SameAccount(Exception):
    pass


class DifferentBanks(Exception):
    pass


class InsufficientFunds(Exception):
    pass


class Account:
    def __init__(self, bank, id):
        self.bank = bank
        self.id = id

    @property
    def balance(self):
        return self.bank.get_balance(self.id)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.bank == other.bank
            and self.id == other.id
        )


class Bank:
    def __init__(self):
        self.bank_acc = {}
        self.transfer_log = []

    def create_account(self, **kwargs):
        acc_num_id = uuid.uuid4()  # Unique account ID
        if 'balance' in kwargs:
            self.bank_acc[acc_num_id] = kwargs['balance']
        else:
            self.bank_acc[acc_num_id] = 0  # Default balance is 0
        return Account(self, acc_num_id)
    
    def get_balance(self, bank_acc):
        return self.bank_acc.get(bank_acc)  # Fixed missing return

    def transfer(self, account1, account2, amount):
        # Check if both accounts are from the same bank
        if account1.bank != account2.bank:
            raise DifferentBanks("Cannot transfer between different banks.")
        
        # Check if both accounts are the same
        if account1 == account2:
            raise SameAccount("Cannot transfer between the same account.")

        # Ensure the amount is positive and there are sufficient funds
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if self.bank_acc[account1.id] < amount:
            raise InsufficientFunds("Insufficient funds for the transfer.")
        
        # Perform the transfer
        self.bank_acc[account1.id] -= amount
        self.bank_acc[account2.id] += amount
        
        # Log the transfer
        self.transfer_log.append((account1, account2, amount))


    

