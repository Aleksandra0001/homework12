from datetime import datetime
from helpper import check_age
from collections import UserDict
import re
import pickle

FILE_NAME = "address_book.bin"
PHONE_REGEX = re.compile(r"^\+?(\d{2})?\(?(0\d{2})\)?(\d{7}$)")


class AddressBook(UserDict):
    def add_record(self, record):
        name = str(record.name)
        self.data[name] = record

    def find_record(self, search_value):
        for record in self.data.values():
            list_of_records = str(record).lower().split(" ")
            for word in list_of_records:
                if word == search_value.lower():
                    return print(f"By {search_value} was found: {record} ")
        else:
            return print("Not found")

    def delete_record(self, value):
        value = value[0].upper() + value[1:].lower()
        self.data.__delitem__(value)
        return print(f"Record {value} was deleted")

    def update_record(self, old_value, new_value):
        # old_value = old_value[0].upper() + old_value[1:].lower()
        # new_value = new_value[0].upper() + new_value[1:].lower()
        record_list = (str(value).split(" ") for value in self.data.values())
        for record in record_list:
            if old_value in record:
                index = record.index(old_value)
                record[index] = new_value
                name = record[0][0].upper() + record[0][1:].lower()
                self.data[name] = ' '.join(record)
                self.delete_record(old_value)

                return print(f"{old_value} was replaced with {new_value}")

            return print(f"{old_value} was not found")

        # record_list = (str(value).split(" ") for value in self.data.values())
        # for record in self.data.values():
        #     list_of_records = str(record).lower().split(" ")
        #     for word in list_of_records:
        #         if word == old_value.lower():
        #             index = list_of_records.index(word)
        #             list_of_records[index] = new_value
        #             new_record = " ".join(list_of_records)
        #             name = list_of_records[0]
        #             print(new_record)
        #             print(name)
                    # for name in self.data.keys():
                        # self.data[name] = new_record

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

    def save(self):
        with open(FILE_NAME, "wb") as fh:
            pickle.dump(self.data, fh)

    def load(self):
        try:
            with open(FILE_NAME, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            pass


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

    def __repr__(self):
        result = f"{self.name} {self.phone_number} {self.birthday}"
        return result


class Field:
    def __init__(self, name, phone=None, birthday=None):
        self.__name = None
        self.__phone = None
        self.__birthday = None
        self.__days_to_birthday = None

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
            self.__phone = None
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
        value = value.strip()
        if value not in [None, ""] and check_age(value):
            self.count_days_to_birthday(value)
            self.__birthday = f"{value} {self.__days_to_birthday} days to birthday"

    def count_days_to_birthday(self, value):
        try:
            current_day = datetime.now()
            birthday = datetime.strptime(value, '%d.%m.%Y')
            current_birthday = birthday.replace(year=current_day.year)
            next_birthday = birthday.replace(year=current_day.year + 1)
            current_count = (current_birthday - current_day).days
            next_count = (next_birthday - current_day).days
            days_to_birthday = current_count if current_day.date() < current_birthday.date() else next_count
            self.__days_to_birthday = days_to_birthday
        except ValueError:
            raise Exception("Birthday not valid")


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


def main():
    commands = ["add", "show", "delete", "find", "search", "edit", "update", "change", "exit", "bye", "goodbye"]
    sasha_book = AddressBook()
    sasha_book.load()
    print("Hi!")
    while True:
        command = input("Write your command:").casefold()
        if command in commands:
            if command == "add":
                name = input("Enter fullname:")
                phone_number = input("Enter phone-number:")
                birthday = input("Enter birthday dd.mm.yyyy:")
                record = Record(Name(name), Phone(phone_number), Birthday(birthday))
                sasha_book.add_record(record)
                sasha_book.save()
            if command == "delete":
                name = input("Enter fullname:")
                sasha_book.delete_record(name)
                sasha_book.save()
            if command == "edit" or command == "update" or command == "change":
                old_value = input("Enter name/phone/birthday:")
                new_value = input("Enter new name/phone/birthday:")
                sasha_book.update_record(old_value, new_value)
                sasha_book.save()
            if command == "find" or command == "search":
                value = input("Enter name/phone/birthday for update:")
                sasha_book.find_record(value)
            if command == "show":
                print(sasha_book)
            if command == "exit" or command == "bye" or command == "goodbye":
                print("Goodbye!")
                sasha_book.save()
                break
        else:
            print("Invalid command")


if __name__ == '__main__':
    main()
