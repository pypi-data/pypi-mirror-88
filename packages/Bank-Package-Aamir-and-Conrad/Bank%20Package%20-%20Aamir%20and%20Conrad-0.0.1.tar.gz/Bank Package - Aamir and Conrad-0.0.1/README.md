Group: Conrad Yeung and Aamir Khan  

[![Build Status](https://travis-ci.org/Conrad-Yeung/Data-533-Lab-4.svg?branch=master)](https://travis-ci.org/Conrad-Yeung/Data-533-Lab-4)
### ***Bank*** 
This package can be used to manage bank customers. There are two subpackages accounts and cards. Accounts subpackage is for corporate customers using bank for large transactions. Cards subpackage is for retail customers who would like to use their bank account with card transactions.

Package Usage:  
The main folder contains two jupyter notebooks `Test_Account.ipynb` and `Test_Card.ipynb` that have the code showing interaction with the package modules.  

### ***"accounts"*** subpackage:
Contains modules for initializing and managing bank accounts such as Chequings and Savings accounts. Contains 3 modules: "account" (baseclass),"chequing","saving". Each module contains class, for example in the "chequing" module, a class "Chequing" exists.

***How to use:***
1) Initialize the account: Create an object of the desired account type. Ex: ``` cheq = chequing("Conrad Yeung", initialdeposit = 10000) ```, will create a chequing account under the name Conrad Yeung with a balance of $10000.  
2) Use class methods to access various features. Ex: ```cheq.deposit(1000)```
3) If desired, direct attributes of the account can be accessed like any other object. Ex:```cheq.actype``` or ```cheq.bal```

***Cheat Sheet of attributes/features:***  
1) Attributes of both "Chequing" and "Saving" classes:
   * ```obj.name```: Account holder's name
   * ```obj.ac```: Account number
   * ```obj.bal```: Account balance
   * ```obj.bal_hist```: Account balance history (past 30)
   * ```obj.bal_time```: Times associated with transactions above.
   * ```obj.recent_transact```: Past 30 transactions (deposits and withdraws)
   * ```obj.trans_time```: Times associated with above.
   * ```obj.trans_lim```: Transaction limit (limit per withdraw)
   * ```obj.actype```: Type of account
  * Attributes unique to "Saving" class:
    * ```obj.intrate```: Interest rate 
    * ```obj.fixed_amount```: Amount in fixed deposit
    * ```obj.datestart```: Date fixed deposit started
    * ```obj.dateend```: Date fixed deposit will end
    * ```obj.fix_dep_inprocess```: If a fixed deposit is in process
2. Available functions to both "Chequing" and "Saving" classes
   * ```obj.details()```: Prints account details
   * ```obj.deposit(amount=0)```: Deposit amount into account
   * ```obj.withdraw(amount=0)```: Withdraw amount from account
   * ```obj.summary()```: Shows account details and plot of the past 30 changes in your account balance.
   * ```obj.change_lim(newlim=0)```: Change the transaction limit of the account - will default to 0 and give you a message that the limit needs to be greater than 0.
 * Function unique to "Saving" class:
   * ```obj.setfixdeposit(amount=0,intrate=0.01,test=False)```: Create/Check a fixed depost for the account. The deposit will be locked in for a year and transfer the funds to your balance. The funds will be transfered after the time period when the function is called again (i.e: call the function once the time period is over and the funds will be deposited)  

### ***"cards"*** subpackage:  
a) card (base) class:  

- makePayment (ABSTRACT)  
    Withdraws money from the card and prints new account balance.  
    Payment will be specific to the card type.  
    Sub-classes credit and debit implement this function  
        
- checkCode (INTERNAL FUNCTION)  
    Checks if the entered PIN code is correct  

- changePIN  
    Sets a new PIN for the card, requires old PIN.  

- checkBalance  
    Prints card holder, card account number and current balance  

- checkTransactions  
    Prints summary information of past transactions.  

b) credit (inherits card) class:  

- Inherits – makePayment, changePIN, checkBalance and checkTransactions  

- setCreditLimit  
    Set maximum limit for the credit taken from the account.     

- checkCreditLimit  
    Check maximum limit for the credit taken from the account.    

- setInterestRate  
    Changes the credit card interest rate  

- checkInterestRate  
    Check the credit card interest rate  

- makePayment (OVERLOADED)  
    Make purchase payment at service point and print new account balance.  

- checkTransactions (OVERLOADED)  
    Prints summary information for the credit card balance.  

c) debit (inherits card) class:  

- Inherits – makePayment, changePIN, checkBalance and checkTransactions   

- setTransactionLimit  
    Set maximum limit for the daily amount withdrawn from the account.     

- checkTransactionLimit  
    Check maximum limit for the daily amount withdrawn from the account.         

- changeCardType  
    Changes the type of the card to one of diamond, gold or platinum   

- checkCardType  
    Displays the type of the debit card.    

- makePayment (OVERLOADED)  
    Make purchase payment at service point and print new account balance.   
