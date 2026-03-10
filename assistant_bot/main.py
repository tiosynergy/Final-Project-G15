from __future__ import annotations

from collections.abc import Callable

from assistant_bot.handlers.commands import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    birthdays,
    change_contact,
    show_all,
    show_birthday,
    show_phone,
)
from assistant_bot.models.address_book import AddressBook
from assistant_bot.utils.parser import parse_input
from assistant_bot.utils.storage import load_data, save_data

CommandHandler = Callable[[list[str], AddressBook], str]

COMMANDS: dict[str, CommandHandler] = {
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "add-address": add_address,
    "add-email": add_email,
    "birthdays": birthdays,
}


def main() -> None:
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")
            continue

        handler = COMMANDS.get(command)
        if handler is None:
            print("Invalid command.")
            continue

        print(handler(args, book))


if __name__ == "__main__":
    main()
