from datetime import datetime
from . import card as cc

# Custom Exception Classes
class NegativeValueError(Exception):
    pass

class InvalidPinCodeError(Exception):
    pass

class StaffAuthenticationError(Exception):
    pass


class credit(cc.card):
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
        
    Credit Card Class Attributes:
    -----------
    credit_limit : int
        card maximum credit limit allowed        
    interest_rate : int
        interest percent accrued on the credit amount   
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

    Credit Card Class Methods:
    --------
    setCreditLimit
        Set maximum limit for the credit taken from the account.     

    setInterestRate
        Changes the credit card interest rate

    checkInterestRate
        Check the credit card interest rate

    checkCreditLimit
        Check maximum limit for the credit taken from the account.    

    makePayment (OVERLOADED)
        Make purchase payment at service point and print new account balance. 

    checkTransactions (OVERLOADED)
        Prints summary information for the credit card balance. 
    '''


    def __init__(self, acct_no, acct_title, card_no, card_pin, amount = 0, credit_limit = 0, interest_rate = 0):
        '''
        Parameters
        ----------
        credit_limit : int
            card maximum credit limit allowed        
        interest_rate : int
            interest percent accrued on the credit amount  

        Raises
        ------
        NegativeValueError
            Any negative numeric value is entered 
        '''
        try:
            cc.card.__init__(self, acct_no, acct_title, card_no, card_pin, amount)

            if credit_limit < 0 or interest_rate < 0:
                raise NegativeValueError
            else:
                self.credit_limit = credit_limit
                self.interest_rate = interest_rate      
        
        except NegativeValueError:
            print("Negative value input not allowed!")
        except:
            print("Unexpected error occurred.")
        else:
            print("\tCredit Limit: {}".format(self.credit_limit))
            print("\tInterest Rate: {}".format(self.interest_rate))

                
    def setCreditLimit(self, pin_entered, mgr_code_entered, newlim = 0):
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
                print("Changing account credit limit.")
                print("\tAccount Holder: {}".format(self.acct_title))
                print("\tCard Number: {}".format(self.card_no))
                print("\tCurrent Balance: ${:.2f}".format(self.bal_curr))

            if (newlim is None) | (newlim < 0):
                raise NegativeValueError
            
            if self.credit_limit < newlim:
                print("\tYour card credit limit has increased from ${:.2f} to ${:.2f}.\n".format(self.credit_limit, newlim))
                self.credit_limit = newlim
            elif self.credit_limit > newlim:
                print("\tYour card credit limit has decreased from ${:.2f} to ${:.2f}.\n".format(self.credit_limit, newlim))
                self.credit_limit = newlim
            else:
                print("\tYour card credit limit is already ${:.2f}.\n".format(self.credit_limit))

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


    def checkCreditLimit(self, pin_entered):
        '''
        Check the credit maximum limit of the card.
            
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
                print("Your card credit limit is ${:.2f}.\n".format(self.credit_limit))
                return True
        
        except InvalidPinCodeError:
            print("Invalid pin code!")
        except:
            print("Unexpected error occurred.")


    def setInterestRate(self, pin_entered, mgr_code_entered, newRate):
        '''
        Changes the credit card interest rate
            
        Parameters:
        -----------
        newRate : int/float. 
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
                print("Changing account interest rate.")
                print("\tAccount Holder: {}".format(self.acct_title))
                print("\tCard Number: {}".format(self.card_no))
                print("\tCurrent Balance: ${:.2f}".format(self.bal_curr))

            if (newRate is None) | (newRate < 0):
                raise NegativeValueError
            
            if self.interest_rate < newRate:
                print("\tYour card interest rate has increased from {:.2f}% to {:.2f}%.\n".format(self.interest_rate, newRate))
                self.interest_rate = newRate
            elif self.interest_rate > newRate:
                print("\tYour card interest rate has decreased from {:.2f}% to {:.2f}%.\n".format(self.interest_rate, newRate))
                self.interest_rate = newRate
            else:
                print("\tYour card interest rate is already {:.2f}%.\n".format(self.interest_rate))
        
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


    def checkInterestRate(self, pin_entered):
        '''
        Check the credit card interest rate
            
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
                print("Your card interest rate  is {:.2f}%.\n".format(self.interest_rate))
        
        except InvalidPinCodeError:
            print("Invalid pin code!")
        except:
            print("Unexpected error occurred.")
        else:
            return True


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
            if amount > self.bal_curr + self.credit_limit:
                print("\tYour withdrawl amount {:.2f} is over your credit limit of ${}.\n".format(amount, self.credit_limit))
                print("\tAvailable balance: ${:.2f}.\n".format(self.bal_curr))
            else:
                self.bal_curr = self.bal_curr - amount
                print("\t${:.2f} has been withdrawn from card no. {} at {}.".format(amount, self.card_no, srvc_point))
                print("\tAvailable balance: ${:.2f}.\n".format(self.bal_curr))
                self.trans_hist[timestamp]= [-amount, srvc_point]
        
        except InvalidPinCodeError:
            print("Invalid pin code!")
        except NegativeValueError:
            print("Negative or invalid input amount value!")
        except:
            print("Unexpected error occurred.") 
        else:
            return True


    def checkTransactions(self, pin_entered):
        '''
        OVERLOADED METHOD FROM BASE CLASS
        Prints summary information for the credit card balance.
        Parameters:
        ----------
        pin_entered : int. Must be four digits
        returns : true/successful
        '''
        try:
            cc.card.checkTransactions(self, pin_entered)
            print("\tCurrent Interest Rate: {:.2f}%.".format(self.interest_rate))
            return True
        except:
            print("Unexpected error occurred.")