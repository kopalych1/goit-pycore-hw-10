from models import AddressBook, Record


WELCOME_MESSAGE = f"""\
{"=" * 40}
{"Welcome to the assistant bot!":^40}
{"=" * 40}

Available commands:
* add <username> <phone> - Adds new user, or new phone to the user
* add-birthday <username> <date> - Adds birthday to a user
* change <username> <old_phone> <new_phone> - Change user's phone
* phone <username> - get phone by username
* add-birthday <username> <old_phone> - Adds birthday to user
* show-birthday <username> - Shows user's birthday
* birthdays - Shows upcoming birthdays
* all - print all users
* quit, close - exits the bot
"""


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me a correct number of arguments please"
        except KeyError:
            return "Give me a correct name please"

    return inner


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


@input_error
def add_contact(args: list[str], addressbook: AddressBook):

    if len(args) != 2:
        raise ValueError(f"Incorrect number of arguments: {len(args)} expected: 2")

    name, phone = args

    if name in addressbook:
        rec: Record = addressbook[name]
        if phone in rec.phones:
            return KeyError(f"Contact with name '{name}' already has phone '{phone}'")

        rec.add_phone(phone)
        return "Phone added."

    rec = Record(name)
    rec.add_phone(phone)

    addressbook.add_record(rec)
    return "Contact added."


@input_error
def change_contact(args: list[str], addressbook: AddressBook):

    if len(args) != 3:
        raise ValueError(f"Incorrect number of arguments: {len(args)} expected: 3")

    name, oldphone, newphone = args

    try:
        addressbook[name].edit_phone(oldphone, newphone)
        return f"Contact '{name}' changed"
    except KeyError as e:
        raise KeyError(f"Contact '{name}' not found") from e


@input_error
def all_contacts(addressbook: AddressBook):

    out = f"+={'=' * 20}=+={'=' * 10}=+={'=' * 10}=+\n"
    out += f"| {'Username':20} | {'Phone(s)':10} | {'Birthday':10} |\n"
    out += f"+={'=' * 20}==={'=' * 10}==={'=' * 10}=+\n"
    if not len(addressbook):
        out += f"| {'None':20}   {' ':10}   {' ':10} |\n"

    for contact in addressbook:
        rec: Record = addressbook[contact]
        birthday_str = rec.birthday.value.strftime("%d.%m.%Y") if rec.birthday else ""
        out += f"| {rec.name:20} | {rec.phones[0]:10} | {birthday_str:10} |\n"
        for phone in rec.phones[1:]:
            out += f"| {' ':20} | {phone:10} | {' ' * 10} |\n"
    out += f"+={'=' * 20}==={'=' * 10}==={'=' * 10}=+\n"
    return out


@input_error
def phone_contacts(args: list[str], addressbook: AddressBook):

    if len(args) != 1:
        raise ValueError(f"Incorrect number of arguments: {len(args)} expected: 1")

    name = args[0]

    try:
        rec: Record = addressbook[name]
        return ", ".join(phone.value for phone in rec.phones)
    except KeyError as e:
        raise KeyError(f"Contact '{name}' not found") from e


@input_error
def add_birthday(args: list[str], addressbook: AddressBook):

    if len(args) != 2:
        raise ValueError(f"Incorrect number of arguments: {len(args)} expected: 2")

    name, birthday = args

    try:
        rec: Record = addressbook[name]
        if rec.birthday:
            return "Birthday already set."
        rec.add_birthday(birthday)
    except KeyError as e:
        raise KeyError(f"Contact '{name}' not found") from e
    return "Birthday added."


@input_error
def show_birthday(args: list[str], addressbook: AddressBook):

    if len(args) != 1:
        raise ValueError(f"Incorrect number of arguments: {len(args)} expected: 1")

    name = args[0]

    try:
        rec: Record = addressbook[name]
        return rec.birthday.value.strftime("%d.%m.%Y") if rec.birthday else ""
    except KeyError as e:
        raise KeyError(f"Contact '{name}' not found") from e


@input_error
def birthdays(addressbook: AddressBook):
    bdays: list[dict] = addressbook.get_upcoming_birthdays()

    out = ""
    for bday in bdays:
        out += f"{bday['name']} - {bday['congratulation_date']}"
    return out


def main():
    print(WELCOME_MESSAGE)

    addressbook = AddressBook()

    while True:
        command, *args = parse_input(input("Enter a command: "))

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, addressbook))

        elif command == "change":
            print(change_contact(args, addressbook))

        elif command == "phone":
            print(phone_contacts(args, addressbook))

        elif command == "all":
            print(all_contacts(addressbook))

        elif command == "add-birthday":
            print(add_birthday(args, addressbook))

        elif command == "show-birthday":
            print(show_birthday(args, addressbook))

        elif command == "birthdays":
            print(birthdays(addressbook))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
