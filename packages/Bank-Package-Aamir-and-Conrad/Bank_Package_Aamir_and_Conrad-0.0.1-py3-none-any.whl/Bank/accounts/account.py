from datetime import datetime
from random import randint
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

class NonNegativeError(Exception):
    pass

class NOTAREALNAME(Exception):
#    def __init__(self,name):
#        self.message = "{} is not a real name as it contains numbers. Try again.".format(name)
#        super().__init__(self.message)
    pass

class NOTENOUGHCASH(Exception):
#    def __init__(self,withdraw,balance):
#        self.message = "You do not have enough funds to withdraw ${:.2f}. Current balance is ${:.2f}.".format(withdraw,balance)
#        super().__init__(self.message)
    pass    

class Account:
    '''
    Contains base account class and methods
        
        Attributes:
        -----------
        name : str
            the name of the account holder
        ac : int
            account number
        bal : int/float
            balance of the account
        bal_hist : list of ints/floats
            balance history of account (past 30 changes of balance)
        bal_time : list of datetime (YYYY/MM/DD HH/MM/SS)
            times of balance history
        recent_transact: 
            balance history of account (past 30 transactions)
        trans_time : list of datetime (YYYY/MM/DD HH/MM/SS)
            times of transcations
            
        Methods:
        --------
        details
            Prints account holder, account number and current balance
            
        deposit(amount = 0)
            Deposits money into the account and prints new account balance. 
         
            Parameters:
            ----------
            amount : int/float (optional). Must be positive number.
        
        withdraw(amount=0)
            Withdraws money from the account and prints new account balance. 
            
            Parameters:
            ----------
            amount : int/float (optional). Must be positive number. Must be less than current account balance.
        
        summary
            Prints summary information as well as graph of past 30 changes to your account balance.
    '''
    def __init__(self,name,amount=0):
        '''
        Parameters
        ----------
        name : str
            the name of the account holder
        amount : int/float (optional)
            initial deposit into the account
            must be positive number
        
        Raises
        ------
        NotImplementedError
            When initial deposit is less than 0.
        '''
        
        try: #If amount is Negative or Alphabetic - dont create account
            if amount < 0:
                raise NonNegativeError 
        except NonNegativeError:
            print ("Initial deposit must be non-negative. Please Try again.")
            return
        except TypeError:
            print ("Please enter a numerical value for the initial deposit to your account. Please try again.")
            return
        
        try:
            for i in str(name): #If name contains number - dont create account
                if i.isdigit():
                    raise NOTAREALNAME
        except NOTREALNAME:
            print ("{} is not a real name as it contains numbers. Try again.".format(name))
            return
        
        self.name = name
        self.ac = randint(10000000,99999999)
        self.bal = amount
        self.bal_hist = [amount] #Initialize Balance History
        self.bal_time = [datetime.now().strftime("%Y/%m/%d, %H:%M:%S")] #Initialize Balance History
        self.recent_transact = []
        self.trans_time = []
    
    def details(self):
        '''
        Prints account holder, account number and current balance
        '''
        print("The account holder is: {}.".format(self.name))
        print("The account number is: {}.".format(self.ac))
        print("Your current balance is: ${:.2f}.\n".format(self.bal))
        
    def deposit(self,amount=0):
        '''
        Deposits money into the account and prints new account balance. 
         
        Parameters:
        ----------
        amount : int/float (optional). Must be positive number.
        '''
        try: #If amount is Negative or Alphabetic - dont create account
            if amount < 0:
                raise NonNegativeError 
        except NonNegativeError:
            print ("Deposit must be non-negative. Please Try again.")
            return
        except TypeError:
            print ("Please enter a numerical value for the deposit. Please try again")
            return
        
        self.bal += amount
        timestamp = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        
        print("${:.2f} has been deposited to account {}.".format(amount,self.ac))
        print("Current balance: ${:.2f}.\n".format(self.bal))
        
        if len(self.bal_hist) < 30: #Record Balance
            self.bal_hist.append(self.bal)
            self.bal_time.append(timestamp)
        else:
            self.bal_hist.pop(0)
            self.bal_time.pop(0)
            self.bal_hist.append(self.bal)
            self.bal_time.append(timestamp)            
            
        if len(self.recent_transact) < 30: #Recent Transactions
            self.recent_transact.append(amount)
            self.trans_time.append(timestamp)
        else:
            self.recent_transact.pop(0)
            self.trans_time.pop(0)
            self.recent_transact.append(amount)
            self.trans_time.append(timestamp)
    
    def withdraw(self,amount=0):
        '''
        Withdraws money from the account and prints new account balance. 
         
        Parameters:
        ----------
        amount : int/float (optional). Must be positive number.
        '''
        try: #If amount is Negative or Alphabetic - dont create account
            if amount < 0:
                raise NonNegativeError 
        except NonNegativeError:
            print ("Withdraw must be non-negative. Please Try again.")
            return
        except TypeError:
            print ("Please enter a numerical value for the withdraw. Please try again")
            return
            
        timestamp = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        
        try:
            if amount > self.bal:
                raise NOTENOUGHCASH
        except NOTENOUGHCASH:
            print ("You do not have enough funds to withdraw ${:.2f}. Current balance is ${:.2f}.".format(amount,self.bal))
            return

        self.bal-=amount
        print("${:.2f} has been withdrawn from account {}.".format(amount,self.ac))
        print("Current balance: ${:.2f}.\n".format(self.bal))
            
        if len(self.bal_hist) < 30: #Record Balance 
            self.bal_hist.append(self.bal)
            self.bal_time.append(timestamp)
        else:
            self.bal_hist.pop(0)
            self.bal_time.pop(0)
            self.bal_hist.append(self.bal)
            self.bal_time.append(timestamp)
                
        if len(self.recent_transact) < 30: #Recent Transactions
            self.recent_transact.append(-amount)
            self.trans_time.append(timestamp)
        else:
            self.recent_transact.pop(0)
            self.trans_time.pop(0)
            self.recent_transact.append(-amount)
            self.trans_time.append(timestamp)
            
    def summary(self):
        '''
        Prints summary information as well as graph of past 30 changes to your account balance.
        '''
        print("Account Holder: {}.".format(self.name))
        print("Current Balance: ${:.2f}.".format(self.bal))
        print("Your balance history for the past 30 transcations:\n")
        
        #Create Plot of Balance
        fig,ax = plt.subplots()
        x = np.arange(1,len(self.bal_hist)+1)
        
        ax.plot(x,self.bal_hist,marker="o")
        ax.set_xticks(x)
        plt.xticks(rotation=90)
        ax.set_xticklabels(self.bal_time)
        formatter = ticker.FormatStrFormatter('$%1.2f')
        ax.yaxis.set_major_formatter(formatter)
        ax.grid()
        
        plt.title("Account balance over past 30 transactions")
        plt.xlabel("Date and time of transcation (YYYY/MM/DD HH:MM:SS)")
        plt.ylabel("Account balance")
        print("\n")