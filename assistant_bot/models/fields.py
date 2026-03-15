from __future__ import annotations

from datetime import datetime, date
import re


class Field:
    """Base value object for contact-related fields.

    Attributes:
        value: Raw stored value for the field.
    """

    def __init__(self, value: object) -> None:
        """Initialize a generic field.

        Args:
            value: Field value of any supported type.
        """
        self.value = value

    def __str__(self) -> str:
        """Return string representation of the stored field value.

        Returns:
            Human-readable field value.
        """
        return str(self.value)


class Name(Field):
    """Contact name field."""

    pass


class Address(Field):
    """Contact address field with non-empty string validation."""

    def __init__(self, value: str) -> None:
        """Initialize and validate an address value.

        Args:
            value: Address text.

        Errors:
            Raises ValueError if address is empty or invalid.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Address cannot be empty")

        formatted_address = value.strip().title()
        super().__init__(formatted_address)


class Email(Field):
    """Email field validated by regular expression."""

    def __init__(self, value: str) -> None:
        """Initialize and validate an email address.

        Args:
            value: Email text in local@domain format.

        Errors:
            Raises ValueError if email format is invalid.
        """
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format. Use example@domain.com")
        super().__init__(value)


class Phone(Field):
    """Phone field that accepts exactly 10 digits."""

    def __init__(self, value: str) -> None:
        """Initialize and validate a phone number.

        Args:
            value: Phone text expected to contain exactly 10 digits.

        Errors:
            Raises ValueError if phone is not 10 digits.
        """
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("10")
        super().__init__(value)


class Birthday(Field):
    """Birthday field stored as a date and rendered as DD.MM.YYYY."""

    value: date

    def __init__(self, value: str) -> None:
        """Initialize and validate birthday date string.

        Args:
            value: Date string in DD.MM.YYYY format.

        Errors:
            Raises ValueError if date format is invalid.
        """
        try:
            dt = datetime.strptime(value, "%d.%m.%Y")
            self.value = dt.date()
        except ValueError as exc:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from exc

    def __str__(self) -> str:
        """Return birthday in DD.MM.YYYY format.

        Returns:
            Formatted birthday string.
        """
        return self.value.strftime("%d.%m.%Y")
