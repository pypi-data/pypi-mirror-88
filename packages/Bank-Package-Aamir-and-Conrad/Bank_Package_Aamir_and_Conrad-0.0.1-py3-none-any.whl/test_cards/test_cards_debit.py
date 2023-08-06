import unittest
from datetime import datetime

import Bank.cards.debit as card_debit

class TestDebitCard(unittest.TestCase):         # test class
    def setUp(self):
        print('TestDebitCard: Set up')

    def tearDown(self):
        print('TestDebitCard: Tear down')

    @classmethod
    def setUpClass(cls):
        print("TestDebitCard: Creating 'debit' class objects")
        # initialize account (acct_no, acct_title, card_no, card_pin, amount)
        cls.debit_card1 = card_debit.debit(1214, 'debit card customer 1', 10007, 1234, 20000)
        cls.debit_card2 = card_debit.debit(1215, 'debit card customer 2', 10008, 4321, 10500)

    @classmethod
    def tearDownClass(cls):
        print('TestDebitCard: tearDownClass')

    # Verify setting daily transaction limit function
    def test_setTransactionLimit(self):
        c1 = self.debit_card1._card__card_pin
        c2 = self.debit_card2._card__card_pin
        self.debit_card1.setTransactionLimit(c1, 7777, 2500)
        self.debit_card2.setTransactionLimit(c2, 7777, 3500)
        self.assertEqual(self.debit_card1.daily_trans_limit, 2500)
        self.assertEqual(self.debit_card2.daily_trans_limit, 3500)
        print("TestDebitCard: Function setTransactionLimit testing ... Successful")

    # Verify changing card type function
    def test_changeCardType(self):
        c1 = self.debit_card1._card__card_pin
        c2 = self.debit_card2._card__card_pin
        self.debit_card1.changeCardType(c1, 7777, "Gold")
        self.debit_card2.changeCardType(c2, 7777, "Platinum")
        self.assertEqual(self.debit_card1.card_type, "Gold")
        self.assertEqual(self.debit_card2.card_type, "Platinum")
        print("TestDebitCard: Function changeCardType testing ... Successful")
