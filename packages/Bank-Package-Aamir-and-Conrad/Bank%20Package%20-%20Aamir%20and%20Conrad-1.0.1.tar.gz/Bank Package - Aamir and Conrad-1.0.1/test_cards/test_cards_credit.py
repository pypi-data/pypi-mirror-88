import unittest
from datetime import datetime

import Bank.cards.credit as card_credit

class TestCreditCard(unittest.TestCase):         # test class
    def setUp(self):
        print('---TestCreditCard: Set up')

    def tearDown(self):
        print('---TestCreditCard: Tear down')

    @classmethod
    def setUpClass(cls):
        print("---TestCreditCard: Creating 'credit' class objects")
        # initialize account (acct_no, acct_title, card_no, card_pin, amount)
        cls.credit_card1 = card_credit.credit(1214, 'credit customer 1', 12140000, 1234, 2000)
        cls.credit_card2 = card_credit.credit(1215, 'credit customer 2', 12150000, 4321, 1500)

    @classmethod
    def tearDownClass(cls):
        print('---TestCreditCard: tearDownClass')

    # Verify setting credit limit function
    def test_setCreditLimit(self):
        c1 = self.credit_card1._card__card_pin
        c2 = self.credit_card2._card__card_pin
        self.assertEqual(self.credit_card1.setCreditLimit(c1, 7777, 1500),True)
        self.assertEqual(self.credit_card2.setCreditLimit(c2, 7777, 500),True)
        self.assertEqual(self.credit_card1.credit_limit, 1500)
        self.assertEqual(self.credit_card2.credit_limit, 500)

        self.assertEqual(self.credit_card1.setCreditLimit(1111, 7777, 7),None)
        self.assertEqual(self.credit_card2.setCreditLimit(1111, 7777, 0),None)
        self.assertEqual(self.credit_card1.setCreditLimit(c1, 1111, 7),None)
        self.assertEqual(self.credit_card2.setCreditLimit(c2, 1111, 0),None)
        print("---TestCreditCard: Function setCreditLimit testing ... Successful")

    # Verify checkCreditLimit function
    def test_checkCreditLimit(self):
        c1 = self.credit_card1._card__card_pin
        c2 = self.credit_card2._card__card_pin
        self.assertEqual(self.credit_card1.checkCreditLimit(c1),True)
        self.assertEqual(self.credit_card2.checkCreditLimit(c2),True)
        print("---TestCreditCard: Function checkCreditLimit testing ... Successful")


    # Verify setting interest rate function
    def test_setInterestRate(self):
        c1 = self.credit_card1._card__card_pin
        c2 = self.credit_card2._card__card_pin
        self.assertEqual(self.credit_card1.setInterestRate(c1, 7777, 7),True)
        self.assertEqual(self.credit_card2.setInterestRate(c2, 7777, 0),True)
        self.assertEqual(self.credit_card1.interest_rate, 7)
        self.assertEqual(self.credit_card2.interest_rate, 0)

        self.assertEqual(self.credit_card1.setInterestRate(1111, 7777, 7),None)
        self.assertEqual(self.credit_card2.setInterestRate(1111, 7777, 0),None)
        self.assertEqual(self.credit_card1.setInterestRate(c1, 1111, 7),None)
        self.assertEqual(self.credit_card2.setInterestRate(c2, 1111, 0),None)
        print("---TestCreditCard: Function setInterestRate testing ... Successful")

    # Verify checkInterestRate function
    def test_checkInterestRate(self):
        c1 = self.credit_card1._card__card_pin
        c2 = self.credit_card2._card__card_pin
        self.assertEqual(self.credit_card1.checkInterestRate(c1),True)
        self.assertEqual(self.credit_card2.checkInterestRate(c2),True)
        print("---TestCreditCard: Function checkInterestRate testing ... Successful")

    # Verify make payment function
    def test_makePayment(self):
        bal1 = self.credit_card1.bal_curr
        bal2 = self.credit_card2.bal_curr
        c1 = self.credit_card1._card__card_pin
        c2 = self.credit_card2._card__card_pin

        self.assertEqual(self.credit_card1.makePayment(c1, 100, "Testing Unit 1"), True)
        self.assertEqual(self.credit_card2.makePayment(c2, 50, "Testing Unit 2"), True)
        self.assertEqual(self.credit_card1.bal_curr, bal1 - 100)
        self.assertEqual(self.credit_card2.bal_curr, bal2 - 50)
        print("---TestCreditCard: Function makePayment testing ... Successful")

    # Verify checkTransactions function
    def test_checkTransactions(self):
        c1 = self.credit_card1._card__card_pin
        c2 = self.credit_card2._card__card_pin
        self.assertEqual(self.credit_card1.checkTransactions(c1), True)
        self.assertEqual(self.credit_card2.checkTransactions(c2), True)
        print("---TestCreditCard: Function checkTransactions testing ... Successful")

