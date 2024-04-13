from classes import AddressBook, Record, UserView, SimpleView, TableView
import pickle


def input_error(func) -> callable:
    """Decorator function to handle input errors."""
    def inner(*args: list, **kwargs: dict):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Error: Key not found.'
        except ValueError:
            return 'Error: Invalid input format. Please provide the correct argument(s).'
        except IndexError:
            return 'Error: Insufficient arguments. Please provide the correct argument(s).'
        except Exception as e:
            return f'Error: {str(e)}. Please check your input and try again.'
    return inner

@input_error
def parse_input(user_input: str) -> tuple:
    """Parse user input."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args: tuple, book: AddressBook) -> str:
    """Add a new contact or update an existing contact's phone number."""
    name, phone = args
    record = book.find(name)

    if not record:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Phone added"

@input_error
def change_contact(args: tuple, book: AddressBook) -> str:
    """Change an existing contact's phone number."""
    name, old_number, new_number = args
    record = book.find(name)

    if not record:
        return "Contact not found."

    record.edit_phone(old_number, new_number)
    return "Contact updated."

@input_error
def show_phone(args: tuple, book: AddressBook) -> str:
    """Show the phone number(s) of a contact."""
    name = args[0]
    record = book.find(name)

    if not record:
        return "Contact not found."

    return '; '.join(str(phone) for phone in record.phones)

@input_error
def add_birthday(args: tuple, book: AddressBook) -> str:
    """Add a birthday to a contact."""
    name, birthday = args
    record = book.find(name)
    
    if not record:
        return 'User does not exist.'
    
    record.add_birthday(birthday)
    return f"Birthday added."

@input_error
def show_birthday(args: tuple, book: AddressBook) -> str:
    """Show the birthday of a contact."""
    name = args[0]
    record = book.find(name)

    if not record:
        return "Contact not found."

    return record.birthday

@input_error
def show_all_birthdays(book: AddressBook) -> list:
    """Show upcoming birthdays within the next week."""
    return book.get_upcoming_birthdays()

def show_all(book: AddressBook) -> dict:
    """Show all contacts in the address book."""
    if not book:
        return "Book is empty."
    return book

def save_data(book: any, filename: str = "addressbook.pkl") -> None:
    """Save address book data to a file."""
    with open(filename, "wb") as file:
        pickle.dump(book, file)

def load_data(filename: str = "addressbook.pkl") -> any:
    """Load address book data from a file."""
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()

def choose_view() -> UserView:
    """Prompt the user to choose a view."""
    while True:
        choice = input("Choose view (simple/table): ").strip().lower()
        if choice == 'simple':
            return SimpleView()
        elif choice == 'table':
            return TableView()
        else:
            print("Invalid choice. Please choose 'simple' or 'table'.")

def main() -> None:
    """Main function to run the address book application."""
    book = load_data()
    print("Welcome to the assistant bot!")
    view = choose_view()
    view.display_commands()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case 'commands':
                view.display_commands()
            case 'hello':
                view.display_message("How can I help you?")
            case 'add':
                view.display_message(add_contact(args, book))
            case 'change':
                view.display_message(change_contact(args, book))
            case 'phone':
                view.display_message(show_phone(args, book))
            case 'add-birthday':
                view.display_message(add_birthday(args, book))
            case 'show-birthday':
                view.display_message(show_birthday(args, book))
            case 'birthdays':
                view.display_message(show_all_birthdays(book))
            case 'all':
                view.display_message(show_all(book))
            case _:
                view.display_message("Invalid command.")

        save_data(book)

        if command in ['close', 'quit', 'exit']:
            view.display_message("Goodbye!")
            break

if __name__ == '__main__':
    main()
