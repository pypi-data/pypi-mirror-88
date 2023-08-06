from datetime import datetime
from . import account as ac

class SPEND_LESS(Exception):
#    def __init__(self,withdraw,limit):
#        self.message = "You are unable to withdraw ${:.2f}. Current transaction limit is ${:.2f}.".format(withdraw,limit)
#        super().__init__(self.message)
    pass   

class Chequing(ac.Account):
    '''
    Inherits from base class "account". 
        
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
        
        trans_lim: int/float
            max transaction limit
        actype : str
            account type. will always be 'Chequings'
        
            
        Methods:
        --------
        details
            Prints account holder, account number, account type, current balance and transaction limit.
            
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
        
        change_lim(newlim=0)
            Changes the transaction limit of the account.
            
            Parameters:
            -----------
            newlim : int/float. Must be positive number
    '''
    def __init__(self,name,amount=0,maxlimit = 1000):
        '''
        Parameters
        ----------
        name : str
            the name of the account holder
        amount : int/float (optional)
            initial deposit into the account must be positive number
        maxlimit: int/float (optional)
            initial withdrawl limit
            
        Raises
        ------
        NotImplementedError
            When initial deposit or limit is less than 0.
        
        '''

        try: #If amount is Negative or Alphabetic
            if amount < 0:
                raise ac.NonNegativeError 
        except ac.NonNegativeError:
            print ("Initial deposit must be non-negative. Please Try again.")
            return
        except TypeError:
            print ("Please enter a numerical value for the initial deposit to your account. Please try again.")
            return
        
        try: #If maxlim is Negative or Alphabetic
            if maxlimit < 0:
                raise ac.NonNegativeError 
        except ac.NonNegativeError:
            print ("Max limit must be non-negative. Please Try again.")
            return
        except TypeError:
            print ("Please enter a numerical value for the max limit to your account. Please try again.")
            return
        
        try:
            for i in str(name): #If name contains number - dont create account
                if i.isdigit():
                    raise ac.NOTAREALNAME
        except ac.NOTAREALNAME:
            print ("{} is not a real name as it contains numbers. Try again.".format(name))
            return
    
        ac.Account.__init__(self,name,amount)
        self.trans_lim = maxlimit
        self.actype = "Chequings"
    
    def details(self):
        '''
        Prints account holder, account number, account type, current balance and transaction limit.
        '''
        print("The account holder is: {}.".format(self.name))
        print("The account number is: {}.".format(self.ac))
        print("The account type is: {}".format(self.actype))
        print("Your current balance is: ${:.2f}.".format(self.bal))
        print("Your current transaction limit is: ${:.2f}.\n".format(self.trans_lim))
        
    def withdraw(self,amount=0):
        '''
        Withdraws money from the account and prints new account balance. 
            
            Parameters:
            ----------
            amount : int/float (optional). Must be positive number. Must be less than current account balance.
        '''
        try: #If amount is Negative or Alphabetic
            if amount < 0:
                raise ac.NonNegativeError 
        except ac.NonNegativeError:
            print("Withdraw must be non-negative. Please Try again.")
            return
        except TypeError:
            print("Please enter a numerical value for the withdraw to your account. Please try again.")
            return
        
        timestamp = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        
        try:
            if amount > self.trans_lim:
                raise SPEND_LESS
        except SPEND_LESS:
            print("You are unable to withdraw ${:.2f}. Current transaction limit is ${:.2f}.".format(amount,self.trans_lim))
            return
        
        try:
            if amount > self.bal:
                raise ac.NOTENOUGHCASH
        except ac.NOTENOUGHCASH:
            print("You do not have enough funds to withdraw ${:.2f}. Current balance is ${:.2f}.".format(amount,self.bal))
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

    def change_lim(self,newlim = 0):
        '''
        Changes the transaction limit of the account.
            
            Parameters:
            -----------
            newlim : int/float. Must be positive number
        '''
        try:
            if newlim < 0:
                raise ac.NonNegativeError
        except ac.NonNegativeError:
            print("Limit must be non-negative. Please Try again.")
            return
        except TypeError:
            print("Please enter a numerical value for the max limit to your account. Please try again.")
            return
    
        if self.trans_lim < newlim:
            print("Your transaction limit has increased from ${:.2f} to ${:.2f}.\n".format(self.trans_lim,newlim))
            self.trans_lim = newlim
        elif self.trans_lim > newlim:
            print("Your transaction limit has decreased from ${:.2f} to ${:.2f}.\n".format(self.trans_lim,newlim))
            self.trans_lim = newlim
        else:
            print("Your transaction limit is already ${:.2f}.\n".format(self.trans_lim))