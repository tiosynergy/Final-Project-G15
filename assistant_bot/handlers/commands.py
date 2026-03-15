from __future__ import annotations

from datetime import datetime
from typing import cast
import re

from assistant_bot.models.address_book import AddressBook
from assistant_bot.models.record import Record
from assistant_bot.services.birthday_service import get_upcoming_birthdays
from assistant_bot.utils.decorators import input_error

@input_error
def change_name(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Invalid format. Use: change-name [old_name] [new_name]")
    
    old_name, new_name = args[0], args[1]
    
    if book.find(new_name):
        return f"Contact with name '{new_name}' already exists. Please choose a different name."
    
    try:
        book.change_record_name(old_name, new_name)
        return f"Contact name successfully changed from '{old_name}' to '{new_name}'."
    except KeyError:
        return f"Contact '{old_name}' not found."
    
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
        if record.find_phone(phone):
            return f"Phone {phone} is already recorded for {name}."
        record.add_phone(phone)

    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    if len(args) < 3:
        raise ValueError("Invalid format. Use: change [name] [old_phone] [new_phone]")
        
    new_phone = args[-1]
    old_phone = args[-2]
    name = " ".join(args[:-2])
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' not found."
    
    record.edit_phone(old_phone, new_phone)
    return f"Phone for '{name}' changed from {old_phone} to {new_phone}."

@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
   if not args:
        raise ValueError("Missing contact name. Use: delete [name]")

   name = args[0]
   record = book.find(name)
   
   if record is None:
        return f"Contact '{name}' not found."
   
   book.delete(name)
   return f"Contact '{name}' deleted."

@input_error
def delete_phone(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Invalid format. Use: delete-phone [name] [phone]")
    
    name, phone, *_ = args
    record = book.find(name)
    
    if record is None:
        return "Contact not found."
        
    record.remove_phone(phone)
    return f"Phone {phone} removed for {name}."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    if not args:
        raise ValueError("Missing contact name. Use: phone [name]")
        
    name = " ".join(args) # об'єднує всі агременти в одне ім'я
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
    if len(args) < 2:
        raise ValueError("Invalid format. Use: add-birthday [name] [DD.MM.YYYY]")
        
    # Останній — date, все інше — ім'я
    date_str = args[-1]
    name = " ".join(args[:-1])
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    
    record.add_birthday(date_str)
    
    return f"Birthday for {name} added: {date_str}"

@input_error
def change_birthday(args: list[str], book: AddressBook) -> str:
    if len(args) < 3:
        raise ValueError("Invalid format. Use: change-birthday [name] [old_birthday] [new_birthday]")
    
    new_birthday = args[-1]
    old_birthday = args[-2]
    name = " ".join(args[:-2])

    record = book.find(name)
    
    if record is None:
        return f"Contact '{name}' not found."
    
    if record.birthday is None:
        return f"Birthday for '{name}' is not set yet. Please use 'add-birthday' first."
        
    try:
        record.edit_birthday(old_birthday, new_birthday)
        return f"Birthday for {name} successfully changed to {new_birthday}."
    except ValueError as e:
        return str(e)

@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    if not args:
        raise ValueError("Missing contact name. Use: show-birthday [name]")
        
    # name = args[0]
    name = " ".join(args)
    record = book.find(name)

    if record is None:
        return f"Contact {name} not found."

    if record.birthday is None:
        return f"Birthday for {name} not found."

    return f"Birthday for {name}: {record.birthday}"


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
   if not args:
        raise ValueError("Please provide the number of days. Use: birthdays [number]")
   
   number_of_days = args[0]
   
   if not number_of_days.isdigit():
        raise ValueError("The number of days must be an integer.")
   
   upcoming = get_upcoming_birthdays(number_of_days, book)
   
   if not upcoming:
        return f"No upcoming birthdays within the next {number_of_days} days."
   
   birthday_lines = [f"Upcoming birthdays within the next {number_of_days} days:"]
   for bd in upcoming:
        birthday_lines.append(f"{bd['name']}: {bd['congratulation_date']}")
        
        return "\n".join(birthday_lines)


@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Missing name or new address.")
    
    # Об’єднуємо args навпаки в рядок для regex парсингу
    full_args_str = " ".join(args)
    
    # # Використовуєм regex щоб дістати ім'я та адресу в лапках
    # промпт: ім'я (любі символи крім ") + пробіл + "адреса" (в лапках)
    match = re.match(r'^(.*?) "(.+?)"$', full_args_str.strip())
    if not match:
        raise ValueError("Invalid input format. Use: " " for address if it has spaces.")
    
    name = match.group(1).strip()
    address_str = match.group(2).strip()
    
    if not address_str:
        raise ValueError("Address cannot be empty.")
    
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    
    record.add_address(address_str)
    
    return f"Address for {name} added: {address_str}"


@input_error
def change_address(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Missing name or new address.")
 
    full_args_str = " ".join(args)
    
    # Використовуєм regex щоб дістати ім'я та адресу в лапках
    # промпт: ім'я (любі символи крім ") + пробіл + "адреса" (в лапках)
    match = re.match(r'^(.*?) "(.+?)"$', full_args_str.strip())
    if not match:
        raise ValueError("Invalid input format. Use: change-address [name] \"[new_address]\" with quotes for address if it has spaces.")
    
    name = match.group(1).strip()
    new_address_str = match.group(2).strip()
    
    if not new_address_str:
        raise ValueError("Address cannot be empty.")
    
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    
    old_address = str(record.address) if record.address else "none"
    record.add_address(new_address_str)
    
    return f"Address for {name} changed from {old_address} to {new_address_str}."

@input_error
def delete_address(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Invalid format. Use: delete-address [name] [address]")
    
    name = args[0]
    address_to_delete = " ".join(args[1:])
    
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' not found.")
    
    try:
        record.remove_address(address_to_delete)
        return f"Address '{address_to_delete}' successfully removed from contact '{name}'."
    except ValueError as e:
        return str(e)

@input_error
def add_email(args: list[str], book: AddressBook) -> str:
    # останній — email, все інше — ім'я
    email_str = args[-1]
    name = " ".join(args[:-1])
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    
    record.add_email(email_str)
    
    return f"Email for {name} added: {email_str}"

@input_error
def change_email(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Missing name or new email.")
    
    # якщо подвійне ім'я або + прізвище або пробіли: arg[-1] — email, все інше — name
    new_email = args[-1]
    name = " ".join(args[:-1])
    
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    
    old_email = str(record.email) if record.email else "none"
    record.add_email(new_email)
    
    return f"Email for {name} changed from {old_email} to {new_email}."

@input_error
def delete_email(args: list[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Invalid format. Use: delete-email [name] [email]")
    
    # останній — email, все інше — name
    email_to_delete = args[-1]
    name = " ".join(args[:-1])
    
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' not found."
        
    try:
        record.remove_email(email_to_delete)
        return f"Email '{email_to_delete}' successfully removed from contact '{name}'."
    except ValueError as e:
        return str(e)
    
@input_error
def search_contacts(args: list[str], book: AddressBook) -> str:
    if not args:
        raise ValueError("Please provide a keyword to search. Use: search [keyword]")
    
    # Якщо користувач ввів кілька слів (наприклад, "search John Doe"), склеюємо їх в один рядок
    keyword = " ".join(args)
    
    found_records = book.search_contacts(keyword)
    
    if not found_records:
        return f"No contacts found matching '{keyword}'."
    
    result_lines = [f"Found {len(found_records)} contact(s) matching '{keyword}':"]
    
    for record in found_records:
        result_lines.append(str(record))
        
    return "\n".join(result_lines)
