from datetime import datetime
from collections import defaultdict
import pandas as pd

class card:
    manager_pwd = 7777
    '''
    Contains base card class attribute and methods
        
        Attributes:
        -----------
        acct_title : str
            the name of the account holder
        acct_no : int
            account number associated with the card
        card_no : int
            card number
        card_pin : int
            card pin number
        bal_curr : int/float
            current balance of the account
        trans_hist: dictionary with datetime(keys): transaction details(values)
            time/transaction history of account
            
        Methods:
        --------
        makePayment
            Withdraws money from the card and prints new account balance. 
        
        checkCode - INTERNAL FUNCTION
            Checks if the input pin is correct

        changePIN
            Sets a new PIN for the card, requires old PIN.

        checkBalance
            Prints card holder, card account number and current balance
                    
        checkTransactions
            Prints summary information of past transactions.
    '''

    def __init__(self, acct_no, acct_title, card_no, pin_entered, amount = 0):
        '''
        Parameters
        ----------
        acct_title : str
            the name of the account holder
        acct_no : int
            account number associated with the card
        card_no : int
            card number
        pin_entered : int
            card pin number
        amount : int/float (optional)
            initial deposit into the account
        
        Raises
        ------
        NotImplementedError
            When account number/title, card number/pin are not provided.
        '''
        if (acct_no is None) | (acct_title is None) | (card_no is None) | (pin_entered is None):
            raise NotImplementedError("Please provide correct details to create a bank card")
        
        self.acct_title = acct_title
        self.acct_no = acct_no
        self.card_no = card_no
        self.__card_pin = pin_entered
        self.bal_curr = amount
        # Initialize balance records
        self.trans_hist = defaultdict(dict)
        self.trans_hist[datetime.now().strftime("%Y/%m/%d, %H:%M:%S")]= [amount, 'Initialized Account']
        
             
    def makePayment(self, pin_entered, amount, srvc_point="Unknown"):
        # Payment will be specific to the card type.
        # Sub-classes credit and debit implement this function
        pass



    def checkCode(self, pin_entered):
        '''
        INTERNAL FUNCTION
        Checks if the input pin is correct

        Parameters:
        ----------
        pin_entered : int. Must be four digits
        returns : True or False
        '''
        return self.__card_pin == pin_entered


    def changePIN(self, oldPIN, newPIN):
        '''
        Sets a new PIN for the card, requires old PIN.

        Parameters:
        ----------
        oldPIN : int. Must be four digits
        newPIN : int. Must be four digits
        returns : Status, True or False
        '''
        # Customer Authentication
        if (oldPIN is None) | (not self.checkCode(oldPIN)):
            print("Invalid pin code, please try again!")
        else:
            self.__card_pin = newPIN
            print("Card pin code successfully changed!")


    def checkBalance(self, pin_entered):
        '''
        Prints card holder, card account number and current balance

        Parameters:
        ----------
        pin_entered : int. Must be four digits
        returns : int, returns current account balance
        '''

        # Customer Authentication
        if (pin_entered is None) | (not self.checkCode(pin_entered)):
            print("Invalid pin code, please try again!")
        else:
            print("Account Holder: {}".format(self.acct_title))
            print("Card Number: {}".format(self.card_no))
            print("Current Balance: ${:.2f}".format(self.bal_curr))


    def checkTransactions(self, pin_entered):
        '''
        Prints summary information for the card balance.
        Parameters:
        ----------
        pin_entered : int. Must be four digits
        returns : none
        '''

        # Customer Authentication
        if (pin_entered is None) | (not self.checkCode(pin_entered)):
            print("Invalid pin code, please try again!")
        else:
            print("Account Holder: {}".format(self.acct_title))
            print("Current Balance: ${:.2f}".format(self.bal_curr))
            print("Your balance history for the past transcations:\n")
            
            df = pd.DataFrame(self.trans_hist, index=['Amount', 'Card Service Point']).T
            print(df)
            print("Current Available Balance: ${}".format(self.bal_curr))