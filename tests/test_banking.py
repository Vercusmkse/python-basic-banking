import banking
import unittest


class TestBanking(unittest.TestCase):
    def test_simple_transaction(self):
        bank = banking.Bank()
        account1 = bank.create_account(balance=100)
        account2 = bank.create_account()

        bank.transfer(account1, account2, 50)
        self.assertEqual(account1.balance, 50)
        self.assertEqual(account2.balance, 50)

    def test_insufficient_funds(self):
        bank = banking.Bank()
        account1 = bank.create_account(balance=100)
        account2 = bank.create_account()

        with self.assertRaises(banking.InsufficientFunds):
            bank.transfer(account1, account2, 200)

    def test_cannot_transfer_to_same_account(self):
        bank = banking.Bank()
        account1 = bank.create_account(balance=100)

        with self.assertRaises(banking.SameAccount):
            bank.transfer(account1, account1, 50)

    def test_cannot_transfer_between_different_banks(self):
        bank1 = banking.Bank()
        bank2 = banking.Bank()
        account1 = bank1.create_account(balance=100)
        account2 = bank2.create_account()

        with self.assertRaises(banking.DifferentBanks):
            bank1.transfer(account1, account2, 50)

    def test_keeps_transfer_log(self):
        bank = banking.Bank()
        account1 = bank.create_account(balance=100)
        account2 = bank.create_account()

        bank.transfer(account1, account2, 50)
        self.assertEqual(len(bank.transfer_log), 1)
        self.assertEqual(bank.transfer_log[0], (account1, account2, 50))
