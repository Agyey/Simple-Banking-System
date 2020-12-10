from random import randint
from datetime import datetime
import sqlite3


class Account:

    def __init__(self, con, opening_balance: float=0):
        self.card_number: str = self.generate_number()
        self.card_pin: str = self.generate_pin()
        self.balance: float = opening_balance
        self.con = con
        self.logged_in: bool = False
        self.services = [
            {'Balance': 'show_balance'},
            {'Log out': 'logout_account'}
        ]

    @staticmethod
    def generate_number() -> str:
        IIN = "400000"
        CAN = str((hash(datetime.now()) + hash(randint(10**9, 10**10-1))) % 10**9).rjust(9, '0')
        card_number = IIN + CAN
        checksum = Account.generate_checksum(card_number)
        card_number += checksum
        return card_number

    @staticmethod
    def generate_pin() -> str:
        return str((hash(datetime.now()) + hash(randint(0, 10*5-1))) % 10**4).rjust(4, '0')

    @staticmethod
    def generate_checksum(number):
        nums = [int(x) for x in number]
        for i in range(len(nums)):
            if (i+1) % 2:
                nums[i] *= 2
        for i in range(len(nums)):
            if nums[i] > 9:
                nums[i] -= 9
        return str((10 - sum(nums) % 10) % 10)

    def create_account(self):
        cur = self.con.cursor()
        sql = f"INSERT INTO card (number, pin) " \
              f"VALUES ('{self.card_number}', '{self.card_pin}');"
        cur.execute(sql)
        self.con.commit()
        print("\nYour card has been created")
        print("Your card number:")
        print(self.card_number)
        print("Your card PIN:")
        print(self.card_pin+"\n")
        return False

    def login_account(self, credentials: dict) -> bool:
        print("\nYou have successfully logged in!\n")
        self.card_number = credentials['card_number']
        self.card_pin = credentials['card_pin']
        self.balance = credentials['balance']
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

    def __init__(self, con):
        self.open = True
        self.services = [
            {'Create an account': 'create_account'},
            {'Log into an account': 'login_account'}
        ]
        self.con = con

    def is_open(self):
        return self.open

    def open_bank(self):
        self.open = True

    def close_bank(self):
        self.open = False

    def create_account(self):
        account = Account(self.con)
        account.create_account()
        return True

    def login_account(self):
        # Ask User Credentials
        credentials = dict()
        print("\nEnter your card number:")
        credentials['card_number'] = input()
        print("Enter your PIN:")
        credentials['card_pin'] = input()
        cur = self.con.cursor()
        sql = f"SELECT balance FROM card " \
              f"WHERE number = '{credentials['card_number']}' " \
              f"AND pin = '{credentials['card_pin']}';"
        cur.execute(sql)
        result = cur.fetchall()
        if result:
            credentials['balance'] = result[0][0]
            account = Account(self.con)
            account_response = account.login_account(credentials)
            if account_response:
                return account_response
        else:
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


with sqlite3.connect('card.s3db') as con:
    con = sqlite3.connect('card.s3db')
    cur = con.cursor()
    sql = "CREATE TABLE IF NOT EXISTS card(" \
          "id INTEGER PRIMARY KEY AUTOINCREMENT," \
          "number TEXT," \
          "pin TEXT," \
          "balance INTEGER DEFAULT 0);"
    cur.execute(sql)
    con.commit()
    bank = Bank(con)
    bank.open_bank()
    while bank.is_open():
        bank.ask_user()
