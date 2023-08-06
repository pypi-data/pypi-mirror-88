from datetime import datetime
from dateutil.relativedelta import relativedelta

from . import account as ac

class SPEND_LESS(Exception):
#    def __init__(self,withdraw,limit):
#        self.message = "You are unable to withdraw ${:.2f}. Current transaction limit is ${:.2f}.".format(withdraw,limit)
#        super().__init__(self.message)
    pass  

class Saving(ac.Account):
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
            account type will always be 'Savings'
        
        intrate : float
            interest rate
        fixed_amount : int/float
            amount for set for fixed interest
        datestart : datetime 
            date amount is fixed
        dateend : datetime
            date amount is released
        fix_dep_inprocess: int
            limited to 1 fixed deposit at a time
            
        Methods:
        --------
        i) details
            Prints account holder, account number, account type, current balance, transaction limit, current amount fixed, interest rate, when it will be released and how much.
            
        ii) deposit(amount = 0)
            Deposits money into the account and prints new account balance. 
         
            Parameters:
            ----------
            amount : int/float (optional). Must be positive number.
        
        iii) withdraw(amount=0)
            Withdraws money from the account and prints new account balance. 
            
            Parameters:
            ----------
            amount : int/float (optional). Must be positive number. Must be less than current account balance. Must be less than trans_lim.
        
        iv) summary
            Prints summary information as well as graph of past 30 changes to your account balance.
        
        v) change_lim(newlim=0)
            Changes the transaction limit of the account.
            
            Parameters:
            -----------
            newlim : int/float. Must be positive number          
        
        vi) setfixdeposit(amount=0,intrate=0.01,test=False)
            Create fixed deposit or check if one is existing.
            
            Parameters:
            -----------
            amount : int/float. Must be positive number greater than 0.
            intrate : float (default = 0.01). Must be positive number greater than 0.
            test : bool (default = False). Testing parameter for datetime variables
        '''
    def __init__(self,name,amount=0,maxlimit = 1000):
        '''
        Parameters
        ----------
        name : str
            the name of the account holder
        amount : int/float (optional)
            initial deposit into the account must be positive number.
        maxlimit: int/float (optional)
            initial withdrawl limit must be positive number.
            
        Raises
        ------
        NotImplementedError
            When initial deposit, maxlimit is less than 0.
        '''
        try: #If amount is Negative or Alphabetic
            if amount < 0:
                raise ac.NonNegativeError 
        except ac.NonNegativeError:
            print("Initial deposit must be non-negative. Please Try again.")
            return
        except TypeError:
            print("Please enter a numerical value for the initial deposit to your account. Please try again.")
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
        self.actype = "Savings"
        self.intrate = 0.01
        self.fixed_amount = 0
        self.datestart = 0
        self.dateend = 0
        self.fix_dep_inprocess = 0         

    def details(self):
        '''
        Prints account holder, account number, account type, current balance, transaction limit, current amount fixed, interest rate, when it will be released and how much.
        '''
        print("The account holder is: {}.".format(self.name))
        print("The account number is: {}.".format(self.ac))
        print("The account type is: {}".format(self.actype))
        print("Your current balance is: ${:.2f}.".format(self.bal))
        print("Your current transaction limit is: ${:.2f}.".format(self.trans_lim))
        print("--------------------------------------------")
        if self.fix_dep_inprocess == 0:
            print("You currently have no fixed deposits in process.\n")
        else:
            print("You currently have ${:.2f} fixed at an interest rate of {:.2f}%.".format(self.fixed_amount,self.intrate*100))
            print("On {}, ${} will be added to your Savings account.\n".format(self.dateend.strftime("%Y/%m/%d"),self.fixed_amount+(self.fixed_amount*self.intrate)))   
           
    def withdraw(self,amount=0):
        '''
        Withdraws money from the account and prints new account balance. 
            
            Parameters:
            ----------
            amount : int/float (optional). Must be positive number. Must be less than current account balance. Must be less than trans_lim.
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
            
    def change_lim(self,newlim=0):
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
###        
    def setfixdeposit(self,amount=0,intrate=0.01,test=False):
        '''
        Create fixed deposit or check if one is existing.
            
            Parameters:
            -----------
            amount : int/float. Must be positive number greater than 0.
            intrate : float (default = 0.01). Must be positive number greater than 0.
            test : bool (default = False). Testing parameter for datetime variables.
        '''
        today = datetime(datetime.today().year,datetime.today().month,datetime.today().day)
        
        if test == True: #For testing purposes
            self.dateend = today

        try: #If amount is Negative or Alphabetic
            if amount < 0:
                raise ac.NonNegativeError 
        except ac.NonNegativeError:
            print("Fixed deposit must be non-negative. Please Try again.")
            return
        except TypeError:
            print("Please enter a numerical value for your fixed deposit. Please try again.")
            return            
            
        try: #If intrate is Negative or Alphabetic
            if intrate < 0:
                raise ac.NonNegativeError 
        except ac.NonNegativeError:
            print("Interest Rate must be non-negative. Please Try again.")
            return
        except TypeError:
            print("Please enter a numerical value for the Interest Rate of your deposit. Please try again.")
            return            
        
        if self.fix_dep_inprocess == 1 and (today == self.dateend or (today-self.dateend).days >= 0): #Have fixed deposit created - lockin = OVER
            print("Your fixed depot created on {} is complete.\n".format(self.datestart.strftime("%Y/%m/%d")))
            self.deposit(self.fixed_amount+(self.fixed_amount*self.intrate))
            self.fix_dep_inprocess = 0
            self.datestart = 0
            self.dateend = 0
        elif self.fix_dep_inprocess == 1 and (today != self.dateend or (today-self.dateend).days < 0): #Fixed deposit still in progress
            print("You already have a fixed deposit in process. The current amount locked in is ${:.2f} at a rate of {:.2f}%. The amount will be made available on {}.\n".format(self.fixed_amount,self.intrate*100,self.dateend.strftime("%Y/%m/%d")))
        elif self.fix_dep_inprocess == 0: #Creation - no current fixed deposit therefore initialize
            self.datestart = today
            self.dateend = today + relativedelta(years=1)
            self.fix_dep_inprocess = 1
            self.fixed_amount = amount
            self.intrate = intrate
            print("Your deposit of ${:.2f} has been fixed for a year with an interest rate of {:.2f}%.".format(self.fixed_amount,self.intrate*100))
            print("On {}, ${} will be added to your Savings account.\n".format(self.dateend.strftime("%Y/%m/%d"),self.fixed_amount+(self.fixed_amount*self.intrate)))   
