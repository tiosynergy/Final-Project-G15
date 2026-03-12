from __future__ import annotations

from datetime import datetime
from typing import cast

from assistant_bot.models.address_book import AddressBook
from assistant_bot.models.record import Record
from assistant_bot.services.birthday_service import get_upcoming_birthdays
from assistant_bot.utils.decorators import input_error


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    if len(args) > 1:
        phone = args[-1]
        name = " ".join(args[:-1])
    else:
        phone = ""
        name = args[0]
    
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."

    if phone:
        record.add_phone(phone)

    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    
    record.edit_phone(old_phone, new_phone)

    return f"Phone for {name} changed from {old_phone} to {new_phone}."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    
    if not record.phones:
        return f"{name} has no phones."
    
    return f"{name}'s phones: {', '.join(str(p.value) for p in record.phones)}"


@input_error
def show_all(_: list[str], book: AddressBook) -> str:
    if not book.data:
        return "No contacts yet."
    
    lines = [str(record) for record in book.data.values()]
    
    return "\n".join(lines)


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    name, date_str, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    
    record.add_birthday(date_str)
    
    return f"Birthday for {name} added: {date_str}"


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    name, *_ = args
    record = cast(Record, book.find(name))

    if record.birthday is None:
        return f"Birthday for {name} not found."

    return f"Birthday for {name}: {record.birthday}"


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    _ = args
    upcoming = get_upcoming_birthdays(book)
    if not upcoming:
        return "No birthdays to congratulate this week."

    birthday_lines = ["Birthday congratulations for this week:\n"]
    for bd in upcoming:
        congratulation_date = datetime.strptime(
            bd["congratulation_date"],
            "%Y.%m.%d",
        ).strftime("%d.%m.%Y")
        birthday_lines.append(f"{bd['name']}: congratulate on {congratulation_date}")
    
    return "\n".join(birthday_lines)


@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    name = args[0]
    address_str = " ".join(args[1:])
    
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    
    record.add_address(address_str)
    
    return f"Address for {name} added: {address_str}"


@input_error
def add_email(args: list[str], book: AddressBook) -> str:
    name, email_str, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    
    record.add_email(email_str)
    
    return f"Email for {name} added: {email_str}"
