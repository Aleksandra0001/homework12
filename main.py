import datetime
from datetime import date, timedelta
from collections import UserDict
import re
import pickle

FILE_NAME = "address_book.bin"
PHONE_REGEX = re.compile(r"^\+?(\d{2})?\(?(0\d{2})\)?(\d{7}$)")


class AddressBook(UserDict):
    def add_record(self, record):
        name = str(record.name)
        self.data[name] = record

    def search_by_records(self, value):
        return value in self.data.values()

    def iterator(self, n):
        if len(self.data) < n:
            raise Exception(
                f'Amount of records in <Address Book> is less then <n> = {n} you have entered')
        else:
            data_list = list(self.data.items())
            while data_list:
                result = '\n'.join(
                    [f'Contact <{el[0]}> has following contacts {el[1]}' for el in data_list[:n]])
                yield result
                data_list = data_list[n:]


class Record:
    def __init__(self, name, phone_number=None, birthday=None):
        self.phone_number = phone_number
        self.name = name
        self.phones = []
        self.birthday = birthday

    def add_phone_number(self, phone_number):
        self.phones.append(phone_number)
        return self.phones

    def delete_phone_number(self, phone_number):
        self.phones.remove(phone_number)

    def edit_phone_number(self, old_number, new_number):
        for index, phone in enumerate(self.phones):
            if str(phone) == str(old_number):
                self.phones[index] = new_number
                break

    def days_to_birthday(self):
        if not self.birthday:
            return
        now = datetime.date.today()
        if (self.birthday.value.replace(year=now.year) - now).days > 0:
            return (self.birthday.value.replace(year=now.year) - now).days
        return (self.birthday.value.replace(year=now.year + 1) - now).days

    def __repr__(self):
        result = f"Name:{self.name}, Phone-number:{self.phone_number}, Birthday:{self.birthday}"
        return result


class Field:
    def __init__(self, name, phone=None, birthday=None):
        self.__name = None
        self.__phone = None
        self.__birthday = None

    @property
    def name(self):
        return self.__name

    @property
    def phone(self):
        return self.__phone

    @property
    def birthday(self):
        return self.__birthday

    @name.setter
    def name(self, value):
        value = value.strip()
        if value != "":
            self.__name = value[0].upper() + value[1:].lower()
        else:
            raise Exception("Name can`t be empty!")

    @phone.setter
    def phone(self, value):
        value = value.strip()
        if not value:
            return None
        else:
            if bool(re.match(PHONE_REGEX, value)):
                if len(value) == 12:
                    self.__phone = f'+{value}'
                elif len(value) == 10:
                    self.__phone = f'+38{value}'
            else:
                raise Exception(f"Phone number is not valid")

    @birthday.setter
    def birthday(self, value):
        self.__birthday = value


class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def __str__(self):
        return str(self.name)


class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)
        self.phone = phone

    def __str__(self):
        return str(self.phone)


class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)
        self.birthday = birthday

    def __str__(self):
        return str(self.birthday)


def write_to_file(address_book):
    with open(FILE_NAME, "wb") as fh:
        pickle.dump(address_book, fh)


def read_file(file_name):
    try:
        with open(file_name, "rb") as fh:
            return pickle.load(fh)
    except FileNotFoundError:
        return AddressBook()


def main():
    commands = ["add", "show", "delete", "find", "edit", "exit", "bye", "goodbye"]
    sasha_book = read_file(FILE_NAME)
    while True:
        command = input("Write your command:").casefold()
        if command in commands:
            if command == "add":
                name = input("Enter fullname:")
                phone_number = input("Enter phone-number:")
                birthday = input("Enter birthday yyyy/mm/dd:")
                record = Record(Name(name), Phone(phone_number), Birthday(birthday))
                sasha_book.add_record(record)
            if command == "delete":
                name = input("Enter fullname:")
                phone_number = input("Enter phone-number:")
                birthday = input("Enter birthday:")
            if command == "show":
                print(sasha_book)
            if command == "exit" or command == "bye" or command == "goodbye":
                print("Goodbye!")
                write_to_file(sasha_book)
                break
            # else:
            #     print("Invalid command")


if __name__ == '__main__':
    main()