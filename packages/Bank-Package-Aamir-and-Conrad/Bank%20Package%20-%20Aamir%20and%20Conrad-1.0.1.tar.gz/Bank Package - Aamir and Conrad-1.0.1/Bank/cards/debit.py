from datetime import datetime
from . import card as cc

# Custom Exception Classes
class NegativeValueError(Exception):
    pass

class InvalidPinCodeError(Exception):
    pass

class StaffAuthenticationError(Exception):
    pass


class debit(cc.card):
    '''
    Contains credit card class attributes and methods
        
        Base Class Attributes:
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
            
        Debit Card Class Attributes:
        -----------
        daily_trans_limit : int
            daily maximum transaction allowed        
        card_type : string
            card type : diamond, gold, platinum   
        --------  
        --------  
        Base Class Methods:
        --------       
        checkCode - INTERNAL FUNCTION
            Checks if the input pin is correct

        changePIN
            Sets a new PIN for the card, requires old PIN.

        checkBalance
            Prints card holder, card account number and current balance
                    
        checkTransactions
            Prints summary information of past transactions.

        Debit Card Class Methods:
        --------
        setTransactionLimit
            Set maximum limit for the daily amount withdrawn from the account.     

        checkTransactionLimit
            Check maximum limit for the daily amount withdrawn from the account.         

        changeCardType
            Changes the type of the card to one of diamond, gold or platinum   

        checkCardType
            Displays the type of the debit card.  

        makePayment (OVERLOADED)
            Make purchase payment at service point and print new account balance. 
    '''


    def __init__(self, acct_no, acct_title, card_no, card_pin, amount = 0, daily_trans_limit = 500, card_type = 'platinum'):
        '''
        Parameters
        ----------
        daily_trans_limit : int
            daily maximum transaction allowed        
        card_type : string
            card type : diamond, gold, platinum     
        
        Raises
        ------
        NegativeValueError
            Any negative numeric value is entered 
        '''
        try:
            cc.card.__init__(self, acct_no, acct_title, card_no, card_pin, amount)

            if daily_trans_limit < 0:
                raise NegativeValueError
            elif card_type is None:
                raise ValueError
            else:
                self.daily_trans_limit = daily_trans_limit
                self.card_type = card_type

        except NegativeValueError:
            print("Negative value input not allowed!")
        except:
            print("Unexpected error occurred.")
        else:
            print("\tDaily Transaction Limit: {}".format(self.daily_trans_limit))
            print("\tDebit Card Type: {}".format(self.card_type))

                 
    def setTransactionLimit(self, pin_entered, mgr_code_entered, newlim = 0):
        '''
        Changes the credit maximum limit of the card.

        Parameters:
        -----------
        newlim : int/float. 
            Must be positive number
        pin_entered : int. 
            Must be four digits   
        mgr_code_entered: int. 
            Branch Manager Code (same for all objects). Only manager allowed to alter credit limit.
        
        Raises
        ------
        StaffAuthenticationError
            When manager/staff credentials are invalid
        InvalidCredentialsError
            When some information is missing
        NegativeValueError
            Any negative numeric value is entered 
        '''
        try:
            # Manager Authentication
            if (mgr_code_entered is None)|(mgr_code_entered != super().manager_pwd):
                raise StaffAuthenticationError

            # Customer Authentication
            if (pin_entered is None) | (not self.checkCode(pin_entered)):
                raise InvalidPinCodeError
            else:
                print("Changing debit card daily transaction limit.")
                print("\tAccount Holder: {}".format(self.acct_title))
                print("\tCard Number: {}".format(self.card_no))
                print("\tCurrent Balance: ${:.2f}".format(self.bal_curr))

            if (newlim is None) | (newlim < 0):
                raise NegativeValueError
            
            if self.daily_trans_limit < newlim:
                print("\tYour daily transaction limit has increased from ${:.2f} to ${:.2f}.\n".format(self.daily_trans_limit,newlim))
                self.daily_trans_limit = newlim
            elif self.daily_trans_limit > newlim:
                print("\tYour daily transaction limit has decreased from ${:.2f} to ${:.2f}.\n".format(self.daily_trans_limit,newlim))
                self.daily_trans_limit = newlim
            else:
                print("\tYour daily transaction limit is already ${:.2f}.\n".format(self.daily_trans_limit))

        except StaffAuthenticationError:
            print("Unauthorized access. Only branch manager can alter the credit limit!")
        except InvalidPinCodeError:
            print("Invalid pin code!")       
        except NegativeValueError:
            print("Negative or invalid input value!")
        except:
            print("Unexpected error occurred.")
        else:
            return True


    def checkTransactionLimit(self, pin_entered):
        '''
        Check the Transaction maximum limit of the card.

        Parameters:
        -----------
        pin_entered : int. 
            Must be four digits 
    
        Raises
        ------
        InvalidPinCodeError:
            Pin code is missing or wrong        
        '''
        try:
            # Customer Authentication
            if (pin_entered is None) | (not self.checkCode(pin_entered)):
                raise InvalidPinCodeError
            else:
                print("Your card daily transaction limit is ${:.2f}.\n".format(self.daily_trans_limit))
                return self.daily_trans_limit
                
        except InvalidPinCodeError:
            print("Invalid pin code!")
        except:
            print("Unexpected error occurred.")

                
    def changeCardType(self, pin_entered, mgr_code_entered, card_type):
        '''
        Changes the type of the card to one of diamond, gold or platinum

        Parameters:
        -----------
        pin_entered : int. 
            Must be four digits   
        mgr_code_entered: int. 
            Branch Manager Code (same for all objects). Only manager allowed to alter credit limit.
        card_type : string
            Change card type to one of diamond, gold, platinum. Manager access required
                
        Raises
        ------
        StaffAuthenticationError
            When manager/staff credentials are invalid
        InvalidCredentialsError
            When some information is missing
        NegativeValueError
            Any negative numeric value is entered 
        '''
        try:
            # Manager Authentication
            if (mgr_code_entered is None)|(mgr_code_entered != super().manager_pwd):
                raise StaffAuthenticationError

            # Customer Authentication
            if (pin_entered is None) | (not self.checkCode(pin_entered)):
                raise InvalidPinCodeError
            else:
                print("Changing debit card type.")
                print("\tAccount Holder: {}".format(self.acct_title))
                print("\tCard Number: {}".format(self.card_no))
                print("\tCurrent Balance: ${:.2f}".format(self.bal_curr))

            # Set card type
            if (card_type is None):
                print("Enter a valid card type.\n")
                raise ValueError
            elif self.card_type == card_type:
                print("\tYour already have the {} debit card".format(self.card_type))
            else:
                self.card_type = card_type
                print("\tYour debit card type has been set to {}".format(self.card_type))
        
        except StaffAuthenticationError:
            print("Unauthorized access. Only branch manager can alter the credit limit!")
        except InvalidPinCodeError:
            print("Invalid pin code!")       
        except NegativeValueError:
            print("Negative or invalid input value!")
        except:
            print("Unexpected error occurred.")
        else:
            return True


    def checkCardType(self, pin_entered):
        '''
        Displays the type of the debit card.

        Parameters:
        -----------
        pin_entered : int. 
            Must be four digits 
        
        Raises
        ------
        InvalidPinCodeError:
            Pin code is missing or wrong             
        '''
        try:
            # Customer Authentication
            if (pin_entered is None) | (not self.checkCode(pin_entered)):
                raise InvalidPinCodeError
            else:
                print("You have the {} debit card".format(self.card_type))
                return True
        
        except InvalidPinCodeError:
            print("Invalid pin code!")
        except:
            print("Unexpected error occurred.")


    def makePayment(self, pin_entered, amount, srvc_point="Unknown"):
        '''
        OVERLOADED METHOD FROM BASE CLASS
        Make purchase payment at service point and print new account balance. 
         
        Parameters:
        ----------
        pin_entered : int
            card pin number
        amount : int/float
            charged amount (Must be positive number)
        srvc_point: string
            service point where payment was made

        Raises
        ------
        InvalidPinCodeError:
            Pin code is missing or wrong    
        NegativeValueError
            Any negative numeric value is entered        
        '''
        try:
            # Customer Authentication
            if (pin_entered is None) | (not self.checkCode(pin_entered)):
                raise InvalidPinCodeError
            
            if (amount is None) | (amount <= 0):
                print("Invalid amount entered")
                raise NegativeValueError

            timestamp = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")

            print("Attempting to charge payment.")
            if amount > self.bal_curr:
                print("Your withdrawl amount {:.2f} is over your account balance ${}.\n".format(amount, self.bal_curr))
            else:
                self.bal_curr = self.bal_curr - amount
                print("${:.2f} has been withdrawn from card no. {} at {}.".format(amount, self.card_no, srvc_point))
                print("Available balance: ${:.2f}.\n".format(self.bal_curr))
                self.trans_hist[timestamp]= [-amount, srvc_point]
        
        except InvalidPinCodeError:
            print("Invalid pin code!")
        except NegativeValueError:
            print("Negative or invalid input amount value!")
        except:
            print("Unexpected error occurred.")   
        else:
            return True      
