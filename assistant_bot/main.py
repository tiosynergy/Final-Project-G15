from __future__ import annotations

from collections.abc import Callable

from colorama import Fore, Style, init as colorama_init

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
from assistant_bot.handlers.notes_commands import (
    add_note,
    delete_note,
    edit_note,
    search_notes,
    show_note,
    show_notes,
)
from assistant_bot.models.address_book import AddressBook
from assistant_bot.models.notes import NotesManager
from assistant_bot.utils.parser import parse_input
from assistant_bot.utils.storage import load_data, load_notes, save_data, save_notes

CommandHandler = Callable[[list[str], AddressBook, NotesManager], str]


def _contact_handler(
    handler: Callable[[list[str], AddressBook], str],
) -> CommandHandler:
    def wrapped(args: list[str], book: AddressBook, notes: NotesManager) -> str:
        _ = notes
        return handler(args, book)

    return wrapped


def _notes_handler(
    handler: Callable[[list[str], NotesManager], str],
) -> CommandHandler:
    def wrapped(args: list[str], book: AddressBook, notes: NotesManager) -> str:
        _ = book
        return handler(args, notes)

    return wrapped

COMMANDS: dict[str, CommandHandler] = {
    "add": _contact_handler(add_contact),
    "change": _contact_handler(change_contact),
    "phone": _contact_handler(show_phone),
    "all": _contact_handler(show_all),
    "add-birthday": _contact_handler(add_birthday),
    "show-birthday": _contact_handler(show_birthday),
    "add-address": _contact_handler(add_address),
    "add-email": _contact_handler(add_email),
    "birthdays": _contact_handler(birthdays),
    "add-note": _notes_handler(add_note),
    "edit-note": _notes_handler(edit_note),
    "delete-note": _notes_handler(delete_note),
    "show-note": _notes_handler(show_note),
    "show-notes": _notes_handler(show_notes),
    "search-notes": _notes_handler(search_notes),
}


def _bot_print(message: str) -> None:
    # Print bot replies with a leading empty line for better CLI readability.
    print(f"\n{message}")


def main() -> None:
    colorama_init(autoreset=True)
    book = load_data()
    notes = load_notes()
    print(f"{Fore.YELLOW}Welcome to the assistant bot!{Style.RESET_ALL}")

    while True:
        user_input = input(f"\n{Fore.CYAN}Enter a command: {Style.RESET_ALL}").strip()
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            save_notes(notes)
            print(f"{Fore.YELLOW}Good bye!{Style.RESET_ALL}")
            break

        if command == "hello":
            _bot_print("How can I help you?")
            continue

        handler = COMMANDS.get(command)
        if handler is None:
            _bot_print("Invalid command.")
            continue

        _bot_print(handler(args, book, notes))


if __name__ == "__main__":
    main()
