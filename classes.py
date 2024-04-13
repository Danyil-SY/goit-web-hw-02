from datetime import datetime, timedelta
from collections import UserDict
from abc import ABC, abstractmethod
from constants import COMMANDS, MAX_NAME_LENGTH, MAX_PHONE_LENGTH, MAX_BIRTHDAY_LENGTH

class Field:
    """Base class for fields."""

    def __init__(self, value: str):
        """Initialize the Field object."""
        self.value = value

    def __str__(self) -> str:
        """Return a string representation of the field."""
        return str(self.value)

    @property
    def value(self) -> str:
        """Get the value of the field."""
        return self.__value

    @value.setter
    def value(self, value: str):
        """Set the value of the field, performing validation."""
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self.__value = value

    def is_valid(self, value: str) -> bool:
        """Check if the given value is valid."""
        return bool(value)

class Birthday(Field):
    """Represents a birthday field."""

    def is_valid(self, value: str) -> bool:
        """Check if the given value is a valid date format."""
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    @property
    def value(self) -> datetime:
        """Get the value of the birthday."""
        return self.__value
    
    @value.setter
    def value(self, value: str) -> None:
        """Set the value of the birthday, performing validation."""
        if self.is_valid(value):
            self.__value = datetime.strptime(value, "%d.%m.%Y")
        else:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Name(Field):
    """Class representing a name field."""
    
    def is_valid(self, value: str) -> bool:
        """Check if the name value is valid."""
        return bool(value)

class Phone(Field):
    """Class representing a phone number field."""

    def is_valid(self, value: str) -> bool:
        """Check if the phone number value is valid."""
        return isinstance(value, str) and len(value) == 10 and value.isdigit()

class Record:
    """Class representing a record with a name and phone numbers."""

    def __init__(self, name: str):
        """Initialize the Record object."""
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday = None

    def __str__(self) -> str:
        """Return string representation of the record."""
        phones_str = ';'.join(str(p) for p in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "None"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"

    def add_phone(self, phone: str) -> None:
        """Add a phone number to the record."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Remove a phone number from the record."""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit a phone number in the record."""
        if self.find_phone(old_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError("The phone number doesn't exist.")     

    def find_phone(self, phone: str) -> Phone:
        """Find a phone number in the record."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str) -> None:
        """Add birthday to a contact."""
        self.birthday = Birthday(birthday)

class AddressBook(UserDict):
    """Class representing an address book."""

    def add_record(self, record: Record) -> None:
        """Add a record to the address book."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """Find a record in the address book by name."""
        return self.data.get(name)
    
    def delete(self, name: str) -> Record:
        """Delete a record from the address book by name."""
        if self.find(name):
            del self.data[name]

    def get_upcoming_birthdays(self) -> list:
        """Return a list of upcoming birthdays within the next week for each user."""
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday = birthday.replace(year=today.year)
                if birthday < today:
                    birthday = birthday.replace(year=today.year + 1)

                days_until_birthday = (birthday - today).days

                if 0 <= days_until_birthday <= 7:
                    if birthday.weekday() == 5:
                        birthday += timedelta(days=2)
                    elif birthday.weekday() == 6:
                        birthday += timedelta(days=1)

                    upcoming_birthdays.append({
                        'name': record.name.value,
                        'congratulation_date': birthday.strftime('%Y.%m.%d')
                    })

        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

class UserView(ABC):
    """Abstract base class for user views."""

    @abstractmethod
    def display_contacts(self, contacts):
        """Display contacts to the user."""
        pass

    @abstractmethod
    def display_commands(self):
        """Display available commands to the user."""
        pass

    @abstractmethod
    def display_message(self, message):
        """Display a message to the user."""
        pass

class SimpleView(UserView):
    """Concrete implementation of UserView for console interface."""

    def display_contacts(self, contacts) -> None:
        """Display contacts to the user."""
        print("Contacts:")
        for contact in contacts:
            print(contact)

    def display_commands(self) -> None:
        """Display available commands to the user."""
        print(COMMANDS)

    def display_message(self, message) -> None:
        """Display a message to the user."""
        print(message)

class TableView(UserView):
    """Concrete implementation of UserView for table view."""

    def display_contacts(self, contacts) -> None:
        """Display contacts as a table."""
        print("Contacts:")
        if not contacts:
            print("No contacts found.")
            return

        table_width = MAX_NAME_LENGTH + MAX_PHONE_LENGTH + MAX_BIRTHDAY_LENGTH + 10 # 10 - just fix for the table width

        print("-" * table_width)
        print(f"| {'Name':<{MAX_NAME_LENGTH}} | {'Phone Numbers':<{MAX_PHONE_LENGTH}} | {'Birthday':<{MAX_BIRTHDAY_LENGTH}} |")
        print("-" * table_width)

        for contact in contacts.data.values():
            name = contact.name.value
            phones = ';'.join(str(p) for p in contact.phones)
            birthday = str(contact.birthday) if contact.birthday else "None"
            print(f"| {name:<{MAX_NAME_LENGTH}} | {phones:<{MAX_PHONE_LENGTH}} | {birthday:<{MAX_BIRTHDAY_LENGTH}} |")

        print("-" * table_width)

    def display_commands(self) -> None:
        """Display available commands to the user."""
        print(COMMANDS)

    def display_message(self, message) -> None:
        """Display a message to the user."""
        print(message)