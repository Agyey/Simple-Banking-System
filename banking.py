from random import randint
from datetime import datetime

class Account:

    def __init__(self, opening_balance: float=0):
        self.card_number: str = self.generate_number()
        self.card_pin: str = self.generate_pin()
        self.balance: float = opening_balance
        self.logged_in: bool = False
        self.services = [
            {'Balance': 'show_balance'},
            {'Log out': 'logout_account'}
        ]

    @staticmethod
    def generate_number() -> str:
        IIN = "400000"
        CAN = str(hash(datetime.now()) % 10**9).rjust(9,'0')
        checksum = str(randint(0, 9))
        return IIN + CAN + checksum

    @staticmethod
    def generate_pin() -> str:
        return str(randint(0, 10*4-1)).rjust(4,'0')

    def create_account(self):
        print("\nYour card has been created")
        print("Your card number:")
        print(self.card_number)
        print("Your card PIN:")
        print(self.card_pin+"\n")
        return False

    def login_account(self, credentials: dict) -> bool:
        if self.card_number == credentials['card_number'] and self.card_pin == credentials['card_pin']:
            print('\nYou have successfully logged in!\n')
            self.logged_in = True
            return self.ask_user()

    def logout_account(self):
        self.logged_in = False
        print('\nYou have successfully logged out!\n')

    def show_balance(self):
        print(f"\nBalance: {self.balance}\n")

    def ask_user(self):
        while self.logged_in:
            for index, service in enumerate(self.services):
                service_name, function = list(service.items())[0]
                print(f"{index + 1}. {service_name}")
            print("0. Exit")
            try:
                choice = int(input())
                if choice == 0:
                    return 'close_bank'
                elif 0 < choice <= len(self.services):
                    service = self.services[choice-1]
                    service_name, function = list(service.items())[0]
                    getattr(self, function)()
                else:
                    print(f"Enter Values between 0-{len(self.services)}")
            except NameError:
                print(f"Enter Values between 0-{len(self.services)}")
        return True


class Bank:

    def __init__(self):
        self.open = True
        self.services = [
            {'Create an account': 'create_account'},
            {'Log into an account': 'login_account'}
        ]
        self.accounts: list = []

    def is_open(self):
        return self.open

    def open_bank(self):
        self.open = True

    def close_bank(self):
        self.open = False

    def create_account(self):
        account = Account()
        account.create_account()
        self.accounts.append(account)
        return True

    def login_account(self):
        # Ask User Credentials
        credentials = dict()
        print("\nEnter your card number:")
        credentials['card_number'] = input()
        print("Enter your PIN:")
        credentials['card_pin'] = input()
        for account in self.accounts:
            account_response = account.login_account(credentials)
            if account_response:
                return account_response
        print('\nWrong card number or PIN!\n')
        return False

    def ask_user(self):
        for index, service in enumerate(self.services):
            service_name, function = list(service.items())[0]
            print(f"{index+1}. {service_name}")
        print("0. Exit")
        try:
            choice = int(input())
            if choice == 0:
                self.close_bank()
            elif 0 < choice <= len(self.services):
                service = self.services[choice-1]
                service_name, function = list(service.items())[0]
                service_request = getattr(self, function)()
                if service_request == 'close_bank':
                    self.close_bank()
            else:
                print(f"Enter Values between 0-{len(self.services)}")
        except NameError:
            print(f"Enter Values between 0-{len(self.services)}")
bank = Bank()
bank.open_bank()
while bank.is_open():
    bank.ask_user()
