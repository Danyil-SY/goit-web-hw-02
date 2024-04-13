COMMANDS = """
    Commands:
    1. add [name] [phone]: Add a new contact with a name and phone number, or update the phone number for an existing contact.
    2. change [name] [new phone]: Change the phone number for the specified contact.
    3. phone [name]: Show the phone number for the specified contact.
    4. all: Show all contacts in the address book.
    5. add-birthday [name] [date of birth]: Add the date of birth for the specified contact.
    6. show-birthday [name]: Show the date of birth for the specified contact.
    7. birthdays: Show upcoming birthdays within the next week.
    8. hello: Receive a greeting from the bot.
    9. close or exit: Close the program.
    10. commands: Print the list of commands.
"""

MAX_NAME_LENGTH = 10
MAX_PHONE_LENGTH = 15
MAX_BIRTHDAY_LENGTH = 10