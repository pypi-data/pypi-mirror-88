import unittest
from datetime import datetime

import Bank.cards.card as card_base 

class TestBaseCard(unittest.TestCase):         # test class
    def setUp(self):
        print('TestBaseCard: Set up')

    def tearDown(self):
        print('TestBaseCard: Tear down')

    @classmethod
    def setUpClass(cls):
        print("TestBaseCard: Creating 'base cards' class objects")
        cls.base_card1 = card_base.card(1214, 'Base Customer 1', 12141214, 1234, 1000)
        cls.base_card2 = card_base.card(1215, 'Base Customer 2', 12151215, 4321, 0)

    @classmethod
    def tearDownClass(cls):
        print('TestBaseCard: tearDownClass')

    # Verify check pincode function
    def test_checkCode(self):
        c1 = self.base_card1._card__card_pin
        c2 = self.base_card2._card__card_pin
        self.assertEqual(self.base_card1.checkCode(c1), True)
        self.assertEqual(self.base_card2.checkCode(c2), True)
        print("TestBaseCard: Function checkCode testing ... Successful")

    # Verify pincode change function
    def test_changePIN(self):
        self.base_card1.changePIN(1234, 2345)
        self.base_card2.changePIN(4321, 2345)
        self.assertEqual(self.base_card1.checkCode(2345), True)
        self.assertEqual(self.base_card2.checkCode(2345), True)
        print("TestBaseCard: Function changePIN testing ... Successful")

    # Verify initial balance
    def test_balance_init(self):
        # Base class can't alter balance, so we can test initial credit.
        self.assertEqual(self.base_card1.bal_curr, 1000)
        self.assertEqual(self.base_card2.bal_curr, 0)
        print("TestBaseCard: Initial balance testing ... Successful")

