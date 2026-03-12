from __future__ import annotations

from .fields import Address, Birthday, Email, Name, Phone


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None
        self.address: Address | None = None
        self.email: Email | None = None

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        for i, phone in enumerate(self.phones):
            if phone.value == phone_number:
                self.phones.pop(i)
                return
            
        raise ValueError(f"Phone {phone_number} not found")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
            
        raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone_number: str) -> Phone | None:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
            
        return None

    def add_birthday(self, birthday_str: str) -> None:
        self.birthday = Birthday(birthday_str)

    def add_address(self, address_str: str) -> None:
        self.address = Address(address_str)

    def add_email(self, email_str: str) -> None:
        self.email = Email(email_str)

    def __str__(self) -> str:
        phones = ", ".join(str(p.value) for p in self.phones) if self.phones else "no phones"
        birthday_info = f"birthday: {self.birthday}" if self.birthday else ""
        address_info = f"address: {self.address}" if self.address else ""
        email_info = f"email: {self.email}" if self.email else ""
        output_str = f"Contact name: {self.name.value}\nPhones: {phones}\n{birthday_info}\n{address_info}\n{email_info}"

        return output_str.strip()
