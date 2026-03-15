from __future__ import annotations

from colorama import Fore, Style

from .fields import Address, Birthday, Email, Name, Phone


class Record:
    """Aggregate model for one contact and related fields."""

    def __init__(self, name: str) -> None:
        """Create a contact record with required name.

        Args:
            name: Contact name.
        """
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None
        self.address: Address | None = None
        self.email: Email | None = None

    def edit_name(self, new_name: str) -> None:
        """Update contact name.

        Args:
            new_name: New name value.
        """
        self.name = Name(new_name)

    def add_phone(self, phone_number: str) -> None:
        """Add a phone number to the contact.

        Args:
            phone_number: Phone value with expected 10-digit format.

        Errors:
            Raises ValueError if phone format is invalid.
        """
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        """Remove all matching phone numbers.

        Args:
            phone_number: Phone value to remove.
        """
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Replace one existing phone number with a new value.

        Args:
            old_phone: Existing phone value to replace.
            new_phone: New phone value.

        Errors:
            Raises ValueError if old phone is not found or new phone is invalid.
        """
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
            
        raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone_number: str) -> Phone | None: #проглянути
        """Find a phone number in the contact.

        Args:
            phone_number: Phone value to search for.

        Returns:
            Matching Phone object or None.
        """
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
            
        return None

    def add_birthday(self, birthday_str: str) -> None:
        """Set birthday for the contact.

        Args:
            birthday_str: Date in DD.MM.YYYY format.

        Errors:
            Raises ValueError if date format is invalid.
        """
        self.birthday = Birthday(birthday_str)

    def edit_birthday(self, old_birthday: str, new_birthday: str) -> None:
        """Replace birthday value if current birthday matches expected old value.

        Args:
            old_birthday: Expected existing birthday value.
            new_birthday: New birthday value in DD.MM.YYYY format.

        Errors:
            Raises ValueError if old value does not match or new date is invalid.
        """
        if self.birthday and self.birthday.value == old_birthday:
            self.birthday = Birthday(new_birthday)
            return
        raise ValueError(f"Birthday {old_birthday} not found")

    def add_address(self, address_str: str) -> None:
        """Set or replace contact address.

        Args:
            address_str: Address text.

        Errors:
            Raises ValueError if address is empty.
        """
        self.address = Address(address_str)

    def remove_address(self) -> None:
        """Remove contact address.

        Errors:
            Raises ValueError if address is not set.
        """
        if self.address is None:
            raise ValueError("Address not found")
        self.address = None
    
    def add_email(self, email_str: str) -> None:
        """Set or replace contact email.

        Args:
            email_str: Email text.

        Errors:
            Raises ValueError if email format is invalid.
        """
        self.email = Email(email_str)

    def remove_email(self, email_str: str) -> None:
        """Remove email when the provided value matches current email.

        Args:
            email_str: Email value to remove.

        Errors:
            Raises ValueError if email is missing or does not match.
        """
        if self.email and self.email.value == email_str:
            self.email = None
            return
        raise ValueError(f"Email {email_str} not found")

    def __str__(self) -> str:
        """Render record as multiline string for CLI output.

        Returns:
            Formatted contact representation.
        """
        output_str = f"\nContact name: {Fore.GREEN}{self.name.value}{Style.RESET_ALL}"
        output_str += f'\nPhones: {", ".join(str(p.value) for p in self.phones) if self.phones else "no phones"}'
        if self.birthday:
            output_str += f"\nBirthday: {self.birthday}"
        if self.address:
            output_str += f"\nAddress: {self.address}"
        if self.email:
            output_str += f"\nEmail: {self.email}"

        return output_str
