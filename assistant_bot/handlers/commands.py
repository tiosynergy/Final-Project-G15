from __future__ import annotations

import re
from colorama import Fore, Style

from assistant_bot.models.address_book import AddressBook
from assistant_bot.models.record import Record
from assistant_bot.services.birthday_service import get_upcoming_birthdays
from assistant_bot.utils.decorators import input_error

@input_error
def change_name(args: list[str], book: AddressBook) -> str:
    """Rename an existing contact using a separator."""
    
    full_input = " ".join(args)
    
    if " | " not in full_input:
        raise ValueError("Use format: change-name [old name] | [new name]")
    
    parts = full_input.split(" | ")
    old_name = parts[0].strip()
    new_name = parts[1].strip()
    
    if not old_name or not new_name:
        raise ValueError("Both old and new names are required.")
    
    if book.find(new_name):
        return f"Contact '{new_name}' already exists. Choose another name."
    
    try:
        book.change_record_name(old_name, new_name)
        return f"Contact name changed from '{old_name}' to '{new_name}'."
    except KeyError:
        return f"Contact '{old_name}' not found."
    
@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """Create a contact or append a phone to an existing contact.

    Args:
        args: Command arguments containing name and optional phone.
        book: Address book storage.

    Returns:
        A message indicating whether a contact was added or updated.

    Errors:
        Validation errors from command parsing and phone creation are converted by input_error.
    """
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
    """Replace an existing phone number for a contact.

    Args:
        args: Command arguments in the format [name, old_phone, new_phone].
        book: Address book storage.

    Returns:
        A status message describing the update result.

    Errors:
        ValueError from invalid format or phone replacement is converted by input_error.
    """
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
   """Delete a contact by name.

   Args:
       args: Command arguments containing a contact name.
       book: Address book storage.

   Returns:
       A status message indicating whether the contact was deleted.

   Errors:
       ValueError for missing name is converted by input_error.
   """
   if not args:
        raise ValueError("Missing contact name. Use: delete [name]")

   name = " ".join(args).strip()

   record = book.find(name)
   
   if record is None:
        return f"Contact '{name}' not found."
   
   book.delete(name)
   return f"Contact '{name}' deleted."

@input_error
def delete_phone(args: list[str], book: AddressBook) -> str:
    """Remove a phone number from a contact.

    Args:
        args: Command arguments in the format [name, phone].
        book: Address book storage.

    Returns:
        A status message describing the deletion result.

    Errors:
        ValueError from invalid input or missing phone is converted by input_error.
    """
    if len(args) < 2:
        raise ValueError("Invalid format. Use: delete-phone [name] [phone]")
    
    phone = args[-1]
    name = " ".join(args[:-1])
    record = book.find(name)
    
    if record is None:
        return "Contact not found."
        
    record.remove_phone(phone)
    return f"Phone {phone} removed for {name}."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """Show all phone numbers for a contact.

    Args:
        args: Command arguments containing a contact name.
        book: Address book storage.

    Returns:
        Formatted phone list or an explanatory message.

    Errors:
        ValueError for missing name is converted by input_error.
    """
    if not args:
        raise ValueError("Missing contact name. Use: phone [name]")
        
    name = " ".join(args) # join all arguments into a single name
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    
    if not record.phones:
        return f"{name} has no phones."
    
    return f"{name}'s phones: {', '.join(str(p.value) for p in record.phones)}"


_LABEL_WIDTH = max(len(label) for label in ("Contact name:", "Birthday:", "Phones:", "Address:", "Email:"))


def _format_record(record: Record) -> str:
    """Format a contact record for aligned multiline CLI output.

    Args:
        record: Contact record to render.

    Returns:
        A formatted multiline string with aligned labels and values.
    """
    def field(label: str, value: str) -> str:
        return f"{label:<{_LABEL_WIDTH}} {value}"

    colored_name = f"{Fore.GREEN}{record.name.value}{Style.RESET_ALL}"
    block = [field("Contact name:", colored_name)]

    if record.birthday:
        block.append(field("Birthday:", str(record.birthday)))

    phone_value = ", ".join(str(p.value) for p in record.phones) if record.phones else "no phones"
    block.append(field("Phones:", phone_value))

    if record.address:
        block.append(field("Address:", str(record.address)))

    if record.email:
        block.append(field("Email:", str(record.email)))

    return "\n".join(block)


@input_error
def show_all(_: list[str], book: AddressBook) -> str:
    """Render all contacts from the address book.

    Args:
        _: Unused command arguments.
        book: Address book storage.

    Returns:
        Formatted list of all contacts or a message if the book is empty.
    """
    if not book.data:
        return "No contacts yet."

    return "\n\n".join(_format_record(record) for record in book.data.values())


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """Attach a birthday to an existing contact.

    Args:
        args: Command arguments in the format [name, DD.MM.YYYY].
        book: Address book storage.

    Returns:
        A status message describing the result.

    Errors:
        ValueError for invalid format, unknown contact, or invalid date is converted by input_error.
    """
    if len(args) < 2:
        raise ValueError("Invalid format. Use: add-birthday [name] [DD.MM.YYYY]")
        
    # last — date, everything else — name
    date_str = args[-1]
    name = " ".join(args[:-1])
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    
    record.add_birthday(date_str)
    
    return f"Birthday for {name} added: {date_str}"

@input_error
def change_birthday(args: list[str], book: AddressBook) -> str:
    """Replace an existing birthday for a contact.

    Args:
        args: Command arguments in the format [name, old_birthday, new_birthday].
        book: Address book storage.

    Returns:
        A status message with update details.

    Errors:
        ValueError for invalid format or date parsing is converted by input_error.
        Record-level ValueError is handled locally and returned as text.
    """
    
    new_birthday = args[-1]
    old_birthday = args[-2]
    name = " ".join(args[:-2]).strip()

    # Перевіряємо, чи є обидва аргументи датами
    date_pattern = r"^\d{2}\.\d{2}\.\d{4}$"
    if not re.match(date_pattern, old_birthday) or not re.match(date_pattern, new_birthday):
        raise ValueError(f"Invalid dates. Usage: change-birthday {name} DD.MM.YYYY DD.MM.YYYY")

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
    """Show birthday for a given contact.

    Args:
        args: Command arguments containing a contact name.
        book: Address book storage.

    Returns:
        Formatted birthday message or not-found message.

    Errors:
        ValueError for missing name is converted by input_error.
    """
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
   """List upcoming birthdays for the next N days.

   Args:
       args: Command arguments containing one integer-like number of days.
       book: Address book storage.

   Returns:
       Aligned multiline birthday report or an empty-result message.

   Errors:
       ValueError for missing or non-integer day count is converted by input_error.
   """
   if not args:
        raise ValueError("Please provide the number of days. Use: birthdays [number]")
   
   number_of_days = args[0]
   
   if not number_of_days.isdigit():
        raise ValueError("The number of days must be an integer.")
   
   upcoming = get_upcoming_birthdays(number_of_days, book)
   
   if not upcoming:
        return f"No upcoming birthdays within the next {number_of_days} days."

   sorted_upcoming = sorted(upcoming, key=lambda x: x["congratulation_date"])
   name_header = "Name"
   date_header = "Birthday"
   name_width = max(len(name_header), *(len(item["name"]) for item in sorted_upcoming))
   date_width = max(len(date_header), *(len(item["congratulation_date"]) for item in sorted_upcoming))

   birthday_lines = [f"Upcoming birthdays within the next {number_of_days} days:"]
   birthday_lines.append(f"{name_header:<{name_width}}  {date_header:<{date_width}}")
   birthday_lines.append(f"{'-' * name_width}  {'-' * date_width}")

   for bd in sorted_upcoming:
       birthday_lines.append(
          f"{bd['name']:<{name_width}}  {bd['congratulation_date']:<{date_width}}"
       )
        
   return "\n".join(birthday_lines)


@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    """Add an address to a contact.

    Args:
        args: Command arguments in the format [name, "address with spaces"].
        book: Address book storage.

    Returns:
        A status message describing the update.

    Errors:
        ValueError for invalid format, empty address, or missing contact is converted by input_error.
    """
    if len(args) < 2:
        raise ValueError("Missing name or new address.")
    
    # Join args to handle cases where name or address contains spaces. Assume the last argument is the address, and everything before it is the name.
    full_args_str = " ".join(args)
    
    # # Use regex to extract name and address in quotes
    # prompt: name (any characters except ") + space + "address" (in quotes)
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
    """Replace an address for a contact.

    Args:
        args: Command arguments in the format [name, "new address"].
        book: Address book storage.

    Returns:
        A status message with old and new address values.

    Errors:
        ValueError for invalid format, empty address, or missing contact is converted by input_error.
    """
    if len(args) < 2:
        raise ValueError("Missing name or new address.")
 
    full_args_str = " ".join(args)
    
    # Use regex to extract name and address in quotes
    # prompt: name (any characters except ") + space + "address" (in quotes)
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
    """Remove the address assigned to a contact.

    Args:
        args: Command arguments containing a contact name.
        book: Address book storage.

    Returns:
        A status message describing deletion outcome.

    Errors:
        ValueError for invalid input or missing contact/address is converted by input_error.
    """
    if not args:
        raise ValueError("Invalid format. Use: delete-address [name]")

    name = " ".join(args)

    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' not found.")

    try:
        record.remove_address()
        return f"Address successfully removed from contact '{name}'."
    except ValueError as e:
        return str(e)

@input_error
def add_email(args: list[str], book: AddressBook) -> str:
    """Add an email to a contact.

    Args:
        args: Command arguments in the format [name, email].
        book: Address book storage.

    Returns:
        A status message describing the update.

    Errors:
        ValueError for missing contact or invalid email is converted by input_error.
    """
    # last argument is the email, all others are the name
    email_str = args[-1]
    name = " ".join(args[:-1])
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    
    record.add_email(email_str)
    
    return f"Email for {name} added: {email_str}"

@input_error
def change_email(args: list[str], book: AddressBook) -> str:
    """Replace a contact email.

    Args:
        args: Command arguments in the format [name, new_email].
        book: Address book storage.

    Returns:
        A status message with old and new email values.

    Errors:
        ValueError for missing contact or invalid email is converted by input_error.
    """
    if len(args) < 2:
        raise ValueError("Missing name or new email.")
    
    # if it's a double name or has a surname or spaces: arg[-1] — email, everything else — name
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
    """Delete a specific email from a contact.

    Args:
        args: Command arguments in the format [name, email].
        book: Address book storage.

    Returns:
        A status message describing deletion result.

    Errors:
        ValueError for invalid input is converted by input_error.
        Record-level ValueError is handled locally and returned as text.
    """
    if len(args) < 2:
        raise ValueError("Invalid format. Use: delete-email [name] [email]")
    
    # last argument is the email, all others are the name
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
    """Search contacts by keyword across multiple fields.

    Args:
        args: Command arguments containing one or more words as keyword.
        book: Address book storage.

    Returns:
        A formatted list of matched contacts or an empty-result message.

    Errors:
        ValueError for empty keyword is converted by input_error.
    """
    if not args:
        raise ValueError("Please provide a keyword to search. Use: search [keyword]")
    
    # If the user provided multiple words (e.g., "search John Doe"), join them into a single string
    keyword = " ".join(args)
    
    found_records = book.search_contacts(keyword)
    
    if not found_records:
        return f"No contacts found matching '{keyword}'."
    
    result_lines = [f"Found {len(found_records)} contact(s) matching '{keyword}':"]
    result_lines.extend(_format_record(record) for record in found_records)

    return "\n\n".join(result_lines)
