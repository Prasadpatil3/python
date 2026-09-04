class BankAccount:
    def __init__(self, name, account_no, balance):
        self.name = name
        self.account_no = account_no
        self.balance = balance

    
    def deposit(self, amount):
        self.balance += amount
        print(amount, "deposited successfully.")


    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(amount, "withdrawn successfully.")
        else:
            print("Insufficient balance.")

    
    def check_balance(self):
        print("Current Balance:", self.balance)

    
    def display(self):
        print("\nAccount Holder:", self.name)
        print("Account Number:", self.account_no)
        print("Balance:", self.balance)


account1 = BankAccount("Sandesh", 101, 10000)
account2 = BankAccount("Rahul", 102, 15000)


account1.display()
account1.deposit(5000)
account1.withdraw(2000)
account1.check_balance()



account2.display()
account2.deposit(3000)
account2.withdraw(5000)
account2.check_balance()
