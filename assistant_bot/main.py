from __future__ import annotations

from collections.abc import Callable

from colorama import Fore, Style, init as colorama_init

from assistant_bot.handlers.commands import (
    add_contact,
    change_contact,
    delete_contact,
    search_contacts,
    change_name,
    show_phone,
    delete_phone, 
    add_birthday,
    change_birthday,
    show_birthday,
    birthdays,
    add_address,
    change_address,
    delete_address,
    add_email,
    change_email,
    delete_email,
    show_all
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
    "delete": _contact_handler(delete_contact),
    "change-name": _contact_handler(change_name),
    "search": _contact_handler(search_contacts),
    "delete-phone": _contact_handler(delete_phone),
    "phone": _contact_handler(show_phone),
    "add-birthday": _contact_handler(add_birthday),
    "change-birthday": _contact_handler(change_birthday),
    "show-birthday": _contact_handler(show_birthday),
    "birthdays": _contact_handler(birthdays),
    "add-address": _contact_handler(add_address),
    "change-address": _contact_handler(change_address),
    "delete-address": _contact_handler(delete_address),
    "add-email": _contact_handler(add_email), 
    "change-email": _contact_handler(change_email), 
    "delete-email": _contact_handler(delete_email),
    "all": _contact_handler(show_all),
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

        if command == "help":
            CMD_INFO: list[tuple[str, str]] = [
        # --- Contacts ---
        ("add <name> <phone>",                                                                         "Create a new contact or add a phone to existing"), 
        ("change <name> <old_phone> <new_phone>",                                                      "Update a phone number of a contact"),              
        ("delete <name>",                                                                              "Delete an existing contact"),                      
        ("search <keyword>",                                                                           "Find a record by keyword"),                        
        ("delete-phone <name> <old_phone> <new_phone>",                                                "Delete the phone number of a contact"),            
        ("phone <name>",                                                                               "Show all phone numbers of a contact"),             
        ("change <old_name> <new_name>",                                                               "Update contact name"),                             
        ("add-birthday <name> <DD.MM.YYYY>",                                                           "Add a birthday to a contact"),                     
        ("change-birthday <name> <old_birthday(format: DD.MM.YYYY)> <new_birthday(format: DD.MM.YYYY)>", "Replace an existing birthday"),                    
        ("show-birthday <name>",                                                                       "Show the birthday of a contact"),                  
        ("birthdays <number_of_days>",                                                                 "Shows birthdays in specified amount of days"),     
        ("add-address <name> <address>",                                                               "Add an address of a contact"),                     
        ("change-address <name> <address>",                                                            "Update the address of a contact"),                 
        ("delete-address <name> <address>",                                                            "Delete the address of a contact"),                 
        ("add-email <name> <email>",                                                                   "Add an email to a contact"),                       
        ("change-email <name> <email>",                                                                "Update the email of a contact"),                   
        ("delete-email <name> <email>",                                                                "Delete the email of a contact"),                   
        ("all",                                                                                        "Show all saved contacts"),
        
        # --- Notes ---
        ("add-note <text>",                                                                            "Create a new note"),
        ("edit-note <id> <text>",                                                                      "Edit an existing note"),
        ("delete-note <id>",                                                                           "Delete a note"),
        ("show-note <id>",                                                                             "Display a specific note"),
        ("show-notes",                                                                                 "Display all saved notes"),
        ("search-notes <keyword>",                                                                     "Search notes by keyword"),
        
        # --- General ---
        ("hello",                                                                                      "Display greeting message"),
        ("help",                                                                                       "Show this help message"),
        ("exit / close",                                                                               "Save data and close the application"),
    ]
            col_width = max(len(cmd) for cmd, _ in CMD_INFO) + 2
            lines = ["Available commands:\n"]
            sections = [
                ("Contacts",    CMD_INFO[:11]),
                ("Notes",       CMD_INFO[11:17]),
                ("General",     CMD_INFO[17:]),
            ]
            for section_name, items in sections:
                lines.append(f"{Fore.YELLOW}{section_name}:{Style.RESET_ALL}")
                for cmd, desc in items:
                    lines.append(f"  {Fore.CYAN}{cmd:<{col_width}}{Style.RESET_ALL}{desc}")
                lines.append("")
            _bot_print("\n".join(lines))
            continue

        handler = COMMANDS.get(command)
        if handler is None:
            _bot_print("Invalid command.")
            continue

        _bot_print(handler(args, book, notes))


if __name__ == "__main__":
    main()
