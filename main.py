from datetime import datetime, timedelta
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

    def delete_record(self, value):
        value = value[0].upper() + value[1:].lower()
        self.data.__delitem__(value)
        return print(f"Record {value} was deleted")

    def update_record(self, old_value):
        for value in self.data.values():
            value_list = str(value).split(",")
            if old_value in value_list:
                print("eeee")
        # else:
        #     print("Record not found.")

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

    def days_to_birthday(self):
        if self.birthday is not None:
            real_time = datetime.now()
            datetime_birthday = datetime.strptime(str(self.birthday), '%d.%m.%Y')
            this_year_birthday = datetime_birthday.replace(year=real_time.year)
            next_year_birthday = datetime_birthday.replace(
                year=real_time.year + 1)
            this_year_days_count = (this_year_birthday - real_time).days
            next_year_days_count = (next_year_birthday - real_time).days
            result = this_year_days_count if real_time.date(
            ) < this_year_birthday.date() else next_year_days_count
        else:
            result = f'There is no birthday date for contact <{self.name}>'
        return result

    def __repr__(self):
        result = f"{self.name}, {self.phone_number}, {self.birthday}, {self.days_to_birthday()} days to birthday"
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
        real_time = datetime.now()
        datetime_birthday = datetime.strptime(value, '%d.%m.%Y')
        checking_age = real_time.year - datetime_birthday.year
        if checking_age >= 100:
            raise Exception(
                f'Hey, grandpa! You are too old) Check if you have entered correct birthday date.')
        elif real_time.year <= datetime_birthday.year:
            raise Exception(
                f'Hey, baby! You are too young) Check if you have entered correct birthday date.')
        else:
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


def main():
    commands = ["add", "show", "delete", "find", "edit", "update", "change", "exit", "bye", "goodbye"]
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
                value = input("Enter name/phone/birthday for update:")
                sasha_book.update_record(value)
                sasha_book.save()
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
