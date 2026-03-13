from __future__ import annotations

from colorama import Fore, Style

from .fields import Address, Birthday, Email, Name, Phone


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None
        self.address: Address | None = None
        self.email: Email | None = None

    def edit_name(self, new_name: str) -> None:
        self.name = Name(new_name)

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
            
        raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone_number: str) -> Phone | None: #проглянути
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
            
        return None

    def add_birthday(self, birthday_str: str) -> None:
        self.birthday = Birthday(birthday_str)

    def edit_birthday(self, old_birthday: str, new_birthday: str) -> None:
        if self.birthday and self.birthday.value == old_birthday:
            self.birthday = Birthday(new_birthday)
            return
        raise ValueError(f"Birthday {old_birthday} not found")

    def add_address(self, address_str: str) -> None:
        self.address = Address(address_str)

    def remove_address(self, address_str: str) -> None:
        if self.address and self.address.value == address_str:
            self.address = None
            return
        raise ValueError(f"Address {address_str} not found")
    
    def add_email(self, email_str: str) -> None:
        self.email = Email(email_str)

    def remove_email(self, email_str: str) -> None:
        if self.email and self.email.value == email_str:
            self.email = None
            return
        raise ValueError(f"Email {email_str} not found")

    def __str__(self) -> str:
        output_str = f"\nContact name: {Fore.GREEN}{self.name.value}{Style.RESET_ALL}"
        output_str += f'\nPhones: {", ".join(str(p.value) for p in self.phones) if self.phones else "no phones"}'
        if self.birthday:
            output_str += f"\nBirthday: {self.birthday}"
        if self.address:
            output_str += f"\nAddress: {self.address}"
        if self.email:
            output_str += f"\nEmail: {self.email}"

        return output_str
