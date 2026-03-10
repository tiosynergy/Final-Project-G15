from __future__ import annotations

from datetime import datetime, date
import re


class Field:
    def __init__(self, value: object) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class Address(Field):
    def __init__(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Адресса не повинна бути порожньою")
        super().__init__(value)


class Email(Field):
    def __init__(self, value: str) -> None:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format. Use example@domain.com")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str) -> None:
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("10")
        super().__init__(value)


class Birthday(Field):
    value: date

    def __init__(self, value: str) -> None:
        try:
            dt = datetime.strptime(value, "%d.%m.%Y")
            self.value = dt.date()
        except ValueError as exc:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from exc

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")
