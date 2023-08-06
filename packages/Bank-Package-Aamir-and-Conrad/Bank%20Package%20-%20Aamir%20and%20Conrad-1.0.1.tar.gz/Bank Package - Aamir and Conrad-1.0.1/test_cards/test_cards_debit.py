import unittest
from datetime import datetime

import Bank.cards.debit as card_debit

class TestDebitCard(unittest.TestCase):         # test class
    def setUp(self):
        print('---TestDebitCard: Set up')

    def tearDown(self):
        print('---TestDebitCard: Tear down')

    @classmethod
    def setUpClass(cls):
        print("---TestDebitCard: Creating 'debit' class objects")
        # initialize account (acct_no, acct_title, card_no, card_pin, amount)
        cls.debit_card1 = card_debit.debit(1214, 'debit card customer 1', 10007, 1234, 20000)
        cls.debit_card2 = card_debit.debit(1215, 'debit card customer 2', 10008, 4321, 10500)

    @classmethod
    def tearDownClass(cls):
        print('---TestDebitCard: tearDownClass')

    # Verify setting daily transaction limit function
    def test_setTransactionLimit(self):
        c1 = self.debit_card1._card__card_pin
        c2 = self.debit_card2._card__card_pin
        self.assertEqual(self.debit_card1.setTransactionLimit(c1, 7777, 2500),True)
        self.assertEqual(self.debit_card2.setTransactionLimit(c2, 7777, 3500),True)
        self.assertEqual(self.debit_card1.daily_trans_limit, 2500)
        self.assertEqual(self.debit_card2.daily_trans_limit, 3500)
        print("---TestDebitCard: Function setTransactionLimit testing ... Successful")

    # Verify checkTransactionLimit function
    def test_checkTransactionLimit(self):
        c1 = self.debit_card1._card__card_pin
        c2 = self.debit_card2._card__card_pin
        self.assertEqual(self.debit_card1.daily_trans_limit, self.debit_card1.checkTransactionLimit(c1))
        self.assertEqual(self.debit_card2.daily_trans_limit, self.debit_card2.checkTransactionLimit(c2))
        print("---TestDebitCard: Function setTransactionLimit testing ... Successful")

    # Verify changing card type function
    def test_changeCardType(self):
        c1 = self.debit_card1._card__card_pin
        c2 = self.debit_card2._card__card_pin
        self.debit_card1.changeCardType(c1, 7777, "Gold")
        self.debit_card2.changeCardType(c2, 7777, "Platinum")
        self.assertEqual(self.debit_card1.card_type, "Gold")
        self.assertEqual(self.debit_card2.card_type, "Platinum")

        oldval = self.debit_card1.card_type
        self.debit_card1.changeCardType(c1, 7777, None)
        self.assertEqual(self.debit_card1.card_type, oldval)

        oldval = self.debit_card2.card_type
        self.debit_card2.changeCardType(c2, 7777, None)
        self.assertEqual(self.debit_card2.card_type, oldval)

        self.assertEqual(self.debit_card1.changeCardType(1111, 7777, "FAKE"),None)
        self.assertEqual(self.debit_card2.changeCardType(1111, 7777, "FAKE"),None)
        self.assertEqual(self.debit_card1.changeCardType(c1, 1111, "FAKE"),None)
        self.assertEqual(self.debit_card2.changeCardType(c2, 1111, "FAKE"),None)
        print("---TestDebitCard: Function changeCardType testing ... Successful")

    # Verify checkCardType function
    def test_checkCardType(self):
        c1 = self.debit_card1._card__card_pin
        c2 = self.debit_card2._card__card_pin
        self.assertEqual(self.debit_card1.checkCardType(c1),True)
        self.assertEqual(self.debit_card2.checkCardType(c2),True)
        print("---TestDebitCard: Function checkCardType testing ... Successful")

    # Verify make payment function
    def test_makePayment(self):
        bal1 = self.debit_card1.bal_curr
        bal2 = self.debit_card2.bal_curr
        c1 = self.debit_card1._card__card_pin
        c2 = self.debit_card2._card__card_pin

        self.assertEqual(self.debit_card1.makePayment(c1, 100, "Testing Unit 1"), True)
        self.assertEqual(self.debit_card2.makePayment(c2, 50, "Testing Unit 2"), True)
        self.assertEqual(self.debit_card1.bal_curr, bal1 - 100)
        self.assertEqual(self.debit_card2.bal_curr, bal2 - 50)
        print("---TestDebitCard: Function makePayment testing ... Successful")