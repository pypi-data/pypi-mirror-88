"""
 Create a package with functions similar to those you would expect to see in a typical banking system.
    
. . . 
    
Subpackages:
------------
    1) accounts : Contains modules for initializing and managing bank accounts such as Chequings and Savings accounts.
    
    Modules:
    -----------
    a) accounts.account : Contains base account class and methods
        
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
        i) details
            Prints account holder, account number and current balance
            
        ii) deposit(amount = 0)
            Deposits money into the account and prints new account balance. 
         
            Parameters:
            ----------
            amount : int/float (optional). Must be positive number.
        
        iii) withdraw(amount=0)
            Withdraws money from the account and prints new account balance. 
            
            Parameters:
            ----------
            amount : int/float (optional). Must be positive number. Must be less than current account balance.
        
        iv) summary
            Prints summary information as well as graph of past 30 changes to your account balance.
    
    b) accounts.chequing : Inherits from base class "account". 
        
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
        i) details
            Prints account holder, account number, account type, current balance and transaction limit.
            
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
        
    c) accounts.saving : Inherits from base class "account". 
        
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
            
                
        
    
    2) cards : Contains modules for initializing and manging bank cards such as Credit Cards and Debit Cards.


"""


