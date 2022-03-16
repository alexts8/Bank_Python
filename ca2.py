import random

#Class for "Account" - contains methods which will be inherited
# by the two specific types of accounts
class Account(object):

    def __init__(self, accid, name, funds, age, userid, atype):
        """Initialising instances of "Account" """
        self.funds = int(funds)
        self.age = age
        self.name = name
        self.atype = atype
        self.accid = accid
        self.userid = userid


    def __str__(self):
        """Method that declares what will be printed when print is called on an instance of "Account" """
        #declaring string "result" and appending each variable to be displayed to it
        result = "Funds: " + str(self.funds) + "\n"
        result += "Age: " + str(self.age) + "\n"
        result+= "ID: " +str(self.accid)+"\n"
        result+= "User's Name: " +str(self.name)+"\n"
        result+= "Account Type: " +str(self.atype)+"\n"

        return result


    def withdraw(self, amount, file="accountsTransactions.txt"):
        """takes an amount an subtracts this from the current account's "funds" value, and writes this transaction to our transaction file"""

        #error checking for values less than or equal to 0 being entered
        if amount <= 0:
            print("You can only withdraw a positive value")
            return

        #defining overdraw variable; amount able to be overdrawn from Account 
        #if the account is a checking account:
        if self.atype=="c":
          #can be overdrawn to a value of -500
          overdraw=-500
        else:
          #otherwise, no overdrawing (overdraw value is 0)
          overdraw=0

        #if taking the withdrawal from the accounts funds would take it below the overdraw limit, disply error message
        if self.funds-amount < overdraw:
            print("Cannot withdraw: Overdrawn")
            return

        #declaring variables to be written into file; type of transaction (withdrawal)
        # and transaction id
        w = "withdraw"
        tid=(random.randint(00000,99999))
        #assigning transaction type and id, account id, and amount withdrawn to string variable
        transaction = f"\n{w},{amount},{self.accid},{tid}"
        f = open(file, "a")
        #writing this variable to file
        f.write(transaction)
        f.close()

        #subtract amount withdrawn from curreny account's funds & display new balance
        self.funds -= amount
        print("\nNew balance is: " + str(self.funds) + "\n")


    def deposit(self, amount, file="accountsTransactions.txt"):
        """takes an amount an adds this from the current account's "funds" value, and writes this transaction to our transaction file"""

        #error checking for values less than or equal to 0 being entered
        if amount <= 0:
            print("You can only deposit a positive value")
            return

        #declaring variables to be written into file; type of transaction (deposit)
        # and transaction id
        d = "deposit"
        tid=(random.randint(00000,99999))
        #assigning transaction type and id, account id, and amount withdrawn to string variable
        transaction = f"\n{d},{amount},{self.accid},{tid}"
        f = open(file, "a")
        #writing this variable to file
        f.write(transaction)
        f.close()

        #add amount deposited to current account's funds & display new balance
        self.funds += amount
        print("\nNew balance is: " + str(self.funds) + "\n")


    def transfer(self, amount, accid, file="accountsTransactions.txt"):
        """takes an amount an takes this from the current account's "funds" value, and writes this transaction to our transaction file, and writes a second transaction,
        of the funds being transferred to the other specified account"""

        #error checking for values less than or equal to 0 being entered        
        if amount <= 0:
            print("You can only transfer a positive value")
            return

        #transaction types for each transaction being performed
        t1 = "transferfrom"
        t2 = "transferto"
        #transaction ids
        tid=(random.randint(00000,99999))
        tid2=(random.randint(00000,99999))
        #assigning transaction type and id, account id, and amount transferred to string variable
        transaction1 = f"\n{t1},{amount},{self.accid},{tid}"
        transaction2 = f"\n{t2},{amount},{accid},{tid2}"
        f = open(file, "a")
        #writing these transaction variables to transaction file
        f.write(transaction1)
        f.write(transaction2)
        f.close()

        #subtracting amount transferred from current account's funds and printing new balance
        self.funds -= amount
        print("transfer complete" + '\n')
        print("\nNew balance is: " + str(self.funds) + "\n")


    def transactions(self):
        """Accesses the transactions file and searches for transactions
        performed on the account currently logged into,
         and prints these, and the account's balance"""

        #prints current balance
        print("\nBalance:" + str(self.funds) + "\n")
        print("Transactions:\n")
        #opening transactions fie in read mode
        f = open("accountsTransactions.txt", "r")
        #iterate through lines of file
        for line in f:
          #splitting each line by commas into a list
            split_line = line.split(",")
            #method i used frequently for ignoring blank lines, should they occur
            # found here:
            #https://www.daniweb.com/programming/software-development/threads/193441/skipping-blank-lines
            if not line.strip():
                continue
            #if the 3rd attribute of the list (where the accounts id is stored)
            #is equal to the currents account id
            #then this is this account's transaction
            if split_line[2].strip() == self.accid:
              #printing transaction
                print(split_line[0] + " " + split_line[1])


    def getfunds(self, file="accountsTransactions.txt"):
        """method used to make accounts' funds persistent:
        opens the transactions file and searches for any transaction 
        that was performed on the current account, by comparing account IDs,
        and then either adds or subtracts the amount of that transaction from account's
        depending on the type of transaction, to get the correct balance"""

        #declare "result" variable
        result = 0
        #opening transactions file in read mode
        f = open(file, "r")
        #iterate through license
        for line in f:
          #splitting lines into lists
            split_line = line.split(",")
            #skipping blank lines
            if not line.strip():
                continue

            #if a list in the file has the same account id as current account, and is a "deposit"
            if split_line[2].strip() == self.accid and split_line[0].strip(
            ) == "deposit":
                #add the amount to result
                result += int(split_line[1])

            #if a list in the file has the same account id as current account, and is a "withdraw"
            elif split_line[2].strip() == self.accid and split_line[0].strip(
            ) == "withdraw":
                #subtract the amount from result
                result -= int(split_line[1])

            #if a list in the file has the same account id as current account, and is a "transferfrom"
            elif split_line[2].strip() == self.accid and split_line[0].strip(
            ) == "transferfrom":
                #subtract the amount from result
                result -= int(split_line[1])

            #if a list in the file has the same account id as current account, and is a "transferto"
            elif split_line[2].strip() == self.accid and split_line[0].strip(
            ) == "transferto":
                #add the amount to result
                result += int(split_line[1])

            #if a list in the file has the same account id as current account, and is a "grant"
            elif split_line[2].strip() == self.accid and split_line[0].strip(
            ) == "grant":
                #add the amount to result
                result += int(split_line[1])

        #making the account's funds equal to result
        self.funds = result

      

    def delete(self):
        """method for deleting account"""
        try:
            #opening accounts file in read
            with open('accounts.txt', 'r') as f:
                #lines variable is a list of lines
                lines = f.readlines()
                #now open file in write (overwrites current file)
                with open('accounts.txt', 'w') as f:
                  #iterate through list of lines
                    for line in lines:
                      #split each line into list by commas
                        split_line = line.split(",")
                        #skip empty lines
                        if not line.split():
                          continue
                          #write every line to the file, EXCLUDING the one which matches
                          #curren account's id
                        if split_line[0]!=self.accid:
                            f.write(line)
            print("\nAccount Deleted\n")
        #catching errors
        except:
            print("Error Occurred")




#class for SavingsAccount, subclass of Account, inherits its methods and properties 
class SavingsAccount(Account):

    def __init__(self, accid, name, age, funds, userid, atype="s"):
        """initialising savings account classes"""
        #inherits al attributes from account class
        super().__init__(accid, name, age, funds, userid, atype)

    def __str__(self):
        """Method that declares what will be printed when print is called on an instance of "SavingsAccount" """

        print("Savings Acc:")
        #inherits str function from account class
        result = Account.__str__(self)
        return result

    def CreateSavings(self, file="accounts.txt"):
        """method to add the details of a newly created file to the accounts file,
        to make accounts persistent"""

        #opening  accounts file in append mode
        f = open(file, "a")
        #declare "acc" as string with all attributes of account, seperated by commas
        acc = f"\n{self.accid},{self.name},{self.age},{self.funds},{self.atype},{self.userid}"
        #write acc to file and close file
        f.write(acc)
        f.close()




#class for CheckingAccount, subclass of Account inherits its methods and properties
class CheckingAccount(Account):
    def __init__(self, accid, name, age, funds, userid, atype="c"):
        """initialising checking account classes"""
        #inherits all attributes from account class
        super().__init__(accid, name, age, funds, userid, atype)

    def __str__(self):
        """Method that declares what will be printed when print is called on an instance of "CheckingAccount" """

        print("Checking Acc:")
        #inherits str function from account class
        result = Account.__str__(self)
        return result

    def CreateChecking(self, file="accounts.txt"):
        """method to add the details of a newly created file to the accounts file,
        to make accounts persistent"""

        #opening  accounts file in append mode
        f = open(file, "a")
        #declare "acc" as string with all attributes of account, seperated by commas
        acc = f"\n{self.accid},{self.name},{self.age},{self.funds},{self.atype},{self.userid}"
        #write acc to file and close file
        f.write(acc)
        f.close()




#Class for customers - contains methods to add a customer to the file, and str and init methods
class Customer(object):

    def __init__(self, name, age, password, userid):
        """Initialising instance of "Customer"""
        self.age = age
        self.name = name
        self.password = password
        self.userid = userid

    def __str__(self):
        """Method that declares what will be printed when print is called on an instance of "Customer" """

        #declaring string "result" and appending each variable to be displayed to it
        result = "Name: " + self.name + "\n"
        result += "Age: " + str(self.age) + "\n"
        result += "ID: " + str(self.userid) + "\n"

        return result

    def AddCustomer(self, file="customersfile.txt"):
        """Method to add instance of customer's attributes to file, to make customers persistent"""

        #open customers file in append mode
        f = open(file, "a")
        #creating variable "cust" which contains all attributes of
        #instance seperated by commas, as a string
        cust = f"\n{self.userid},{self.name},{self.age},{self.password}"
        #writing "cust" to file and closing file
        f.write(cust)
        f.close()


#Class for the bank's grant system, containing methods to give grants, and load the amount
#left in the funds, from grants file, also contains str and init methods
class GrantFund(object):
  
    def __init__(self, funds=5000):
      """Initialising the grant fund"""

      #funds are always initialised as 5000
      self.funds = funds
    
    def __str__(self):
      """To print the value of the fund"""

      result="Funds Remaining: "+self.funds +"\n"

      return result

    def givegrant(self, amount, accid, file="accountsTransactions.txt"):
      """method to award a grant to an account: takes the value
       from the grant fund and adds it to the account's funds,
        and records these transactions in appropriate files"""


      #error checking for values larger than the grants' available funds
      if amount > self.funds:
        print("\nError: Grant appplied for too large \n")
        return

      #error checking for values of 0 or less
      if amount <= 0:
          print("\nError: You can only enter a positive value\n")
          return

      #adding grant awarded to accounts funds, and subtracting amount from grant fund
      current_acc.funds+=amount
      self.funds-=amount

      #declaring variables for type of transaction and transaction id
      g = "grant"
      tid=(random.randint(00000,99999))
      #assigning transaction type and id, account id, and value of grant to string variable
      transaction = f"\n{g},{amount},{current_acc.accid},{tid}"
      #opening transactions file in append
      f = open(file, "a")
      #writin this variable to transactions file and closing file
      f.write(transaction)
      f.close()

      #opening grants file in append mode
      f = open("grants.txt", "a")
      #declaring amountlost - string variable that contains amount of grant
      amountlost=f"\n{amount}"
      #writing amountlost to file and close file
      f.write(amountlost)
      f.close()

      print("\n Grant Awarded!\n")


    def loadfund(self,file="grants.txt"):
      """Method ran upon execution of program, make sure the grant fund has the
      correct, persistent vaue - accesses grants file and subtracts grants awarded"""

      #opening grants file in read mode
      f=open(file,"r")
      #iterate through each line of file
      for line in f:
          if not line.split():
                continue
          x=line.strip()
        #subtract int value of each line from grant fund
          self.funds -= int(x)
        #close file
      f.close()

        


#creating loop that makes menu repeat
loop = True
while loop:

    #menu function
    def menu():
        """menu that is displayed upon execution of program;
        displays options, and executes code and methods based upon user selection"""

        #creating instance for grant fund
        fund=GrantFund()
        #running "loadfund" on fund - getting correct value for funds
        fund.loadfund()
        #using global variables to prevent errors of undefined variables
        global user
        global current_acc

        #variable used to choose menu option
        x=0
        #execute menu while x = 0 (before valid option picked)
        while x==0:
          #try except to catch errors for invalid types of input
          try:
            #change value of x based on user input
            x = int(
                input(
                    "\nMANAGE USER: \n 1. Login \n 2. Create new User\n 3. Create Account \n\nMANAGE ACCOUNT:\n 4. Sign into Account \n 5. Withdraw\n 6. Deposit\n 7. Transfer\n 8. View Transactions and Balance\n 9. Apply For Grant\n 10. Delete Account\n"
                ))
          except ValueError:
            print("\nInvalid type entered\n")

        #if user entered 1 - login
        if (x == 1):
          #get user input for userid
            userid = input("Enter user id \n")
            #open customer file in read mode
            f = open("customersfile.txt", "r")
            #get user input for password
            passw = input("enter password ")
            for line_str in f:
              #loop throiugh lines of file & split into lists by commas
                split_line = line_str.split(",")
                #skipping blank lines
                if not line_str.split():
                    continue
                    #if the entered userid and password match any password and userid in file
                if split_line[0].strip() == userid and split_line[3].strip(
                ) == passw:
                    #create instance "user" using elements in this matching line
                    user = Customer(split_line[1], split_line[2],
                                    split_line[3], userid)
                    #display success message 
                    print("Logged in as: " + user.name)
 
        #if user input 2 - create new user
        if (x == 2):
            #get values from user for name age and passw
            name = input("Enter name \n")
            age = input("Enter age \n")
            passw = input("Enter password \n")
            #generate userid
            userid = (random.randint(100000000, 999999999))

            #create instance of customer "user" with these variables
            user = Customer(name, age, passw, userid)
            #run AddCustomer on this instance to store it in file
            user.AddCustomer()
            print("New User Added \nYour unique ID for login is:" +
                  str(userid))

        #if user entered 3 - create account
        elif (x == 3):
            #input for type of account to be created
            t = int(input("What type?\n1: Savings\n2: Checking\n"))
            #error checking - displays error if instance "user" doesn't exist
            try:
              #create age variable from user.age
              age = int(user.age)
            except NameError:
              print("\nMust be logged in to make an account!")
              return
            #if user selected to make savings account
            if (t == 1):
                #check that age variable is greater than 14
                if (age < 14):
                    print("Error: Must be over 14 to create a savings account")
                #if age is not <14
                else:
                  #create variables for instance SavingsAccount
                    #generate accid
                    accid = (random.randint(100000000, 999999999))
                    name = user.name
                    funds = 0
                    userid = user.userid
                    #create SavingsAccount instance "savings"
                    savings = SavingsAccount(accid, name, age, funds, userid)
                    #run CreateSavings on this instance to store it in file
                    savings.CreateSavings()
                    print("\nID for login is: " + str(savings.accid) +
                          "\n")
                    return

            #if user selected to create checking account
            elif (t == 2):
               #check that age variable is greater than 14
                if (age < 18):
                    print(
                        "Error: Must be over 18 to create a checking account")
                else:
                    #if age is not <14
                    #create variables for instance CheckingAccount
                    #generate accid
                    accid = (random.randint(100000000, 999999999))
                    name = user.name
                    funds = 0
                    userid = user.userid
                    #create CheckingAccount instance "checking"
                    checking = CheckingAccount(accid, name, age, funds,userid)
                    #run CreateChecking on this instance to store it in file
                    checking.CreateChecking()
                    print("\nID for login is: " + str(checking.accid) +
                          "\n")
                    print("Checking accounts can be overdrawn to a value of -500\n")
                    return

        #if user input 4 - sign into account
        if (x == 4):
            #get user input for accid
            accid = input("Enter ID of account to manage:\n")
            #open accounts file in read mode
            f = open("accounts.txt", "r")
            #try creating variable userid from instace user attribute userid
            try:
              userid=user.userid
              #if we get a NameError
            except NameError:
              #return error and leave function
              print("\nERROR: Must be logged in to access account\n")
              return
              #iterate through lines in file
            for line_str in f:
                #split lines into lists seperated by commas
                split_line = line_str.split(",")
                #skip empty lines
                if not line_str.split():
                    continue
                    #if userid and accid match values in any line, and the account type
                    #field is equal to "s" (element 4 of split_line)
                if split_line[0].strip() == accid and split_line[4].strip(
                ) == "s" and split_line[5].strip()==userid:
                    #create instance current_acc of SavingsAccount
                    #using the matching lines' attributes
                    current_acc = SavingsAccount(split_line[0], split_line[1],
                                                 split_line[2], split_line[3],
                                                 split_line[4])
                    print("\nlogged in as Savings Account:" +
                          str(split_line[0]))
                    current_acc.getfunds()
                    #if userid and accid match values in any line, and the account type
                    #field is equal to "c" (element 4 of split line)
                elif split_line[0].strip() == accid and split_line[4].strip(
                ) == "c" and split_line[5].strip()==userid:
                    #create instance current_acc of CheckingAccount
                    #using the matching lines' attributes
                    current_acc = CheckingAccount(split_line[0], split_line[1],
                                                  split_line[2], split_line[3],
                                                  split_line[4])
                    print("\nlogged in as Checking Account:" +
                          str(split_line[0]))
                    current_acc.getfunds()

        #if user input 5 - wihdraw
        elif (x == 5):
            #user input for amount
            amount = int(input("Enter Amount"))
            #try to execute withdraw method on current_acc, passing amount
            try:
              current_acc.withdraw(amount)
            #if this gives a NameError; display error message
            except NameError:
              print("\nLog into an account first!\n")

        #if user input 6 - deposit
        elif (x == 6):
            #user input for amount
            amount = int(input("Enter Amount"))
            #try to execute deposit method on current_acc, passing amount
            try:
              current_acc.deposit(amount)
              #if this gives a NameError; display error message
            except NameError:
              print("\nLog into an account first!\n")

        #if user input 7 - transfer
        elif (x == 7):
            #user input for amount and accid (id of account to transfer to)
            amount = int(input("\nEnter Amount\n"))
            accid = (input("\nEnter ID of account to transfer to\n"))
            #try to execute transfer method on current_acc, passing amount and accid
            try:
             current_acc.transfer(amount, accid)
             #if this gives a NameError; display error message
            except NameError:
              print("\nLog in to an account first!\n")

        #if user input 8 - view transactions and balance
        elif (x == 8):
          #try to execute tranactions method on current_acc
          try:
            current_acc.transactions()
            #if this gives a NameError; display error message
          except NameError:
            print("\nLog into an account first!\n")

        #if user input - apply for grant
        elif (x == 9):
            #user input for amount
            amount = int(input("\nEnter Amount\n"))
            #try to execute givegrant method on fund, passing amount
            #and current_acc's accid attribute
            try:
             fund.givegrant(amount, current_acc.accid)
             #if this gives a NameError; display error message
            except NameError:
              print("\nLog in to an account first!\n")

        #if user input - delete account
        elif (x == 10):
          #try to execute delete method on current_acc
          try:
            current_acc.delete()
            #delete instance "current_acc"
            del current_acc
            #if this gives a NameError; display error message
          except NameError:
            print("\nLog into an account first!\n")

  #main code
  #execute menu function
    menu()


