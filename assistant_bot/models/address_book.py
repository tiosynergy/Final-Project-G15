from __future__ import annotations

from collections import UserDict

from .record import Record


class AddressBook(UserDict[str, Record]):
    """Dictionary-like storage for contact records keyed by contact name."""

    def add_record(self, record: Record) -> None:
        """Add or replace a contact record.

        Args:
            record: Contact record to store.
        """
        self.data[str(record.name.value)] = record

    def find(self, name: str) -> Record | None:
        """Find a contact by exact name.

        Args:
            name: Contact name key.

        Returns:
            Matching Record or None.
        """
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Delete a contact by name if present.

        Args:
            name: Contact name key.
        """
        self.data.pop(name, None)

    def change_record_name(self, old_name: str, new_name: str) -> None:
        """Rename a contact key and update record name value.

        Args:
            old_name: Existing contact name.
            new_name: New contact name.

        Errors:
            Raises KeyError if the old name does not exist.
        """
        if old_name not in self.data:
            raise KeyError(f"Contact {old_name} not found.")
        
        record = self.data.pop(old_name)

        record.edit_name(new_name)

        self.data[new_name] = record

    def search_contacts(self, keyword: str) -> list:
        """Search contacts by keyword across name, email, address, birthday, and phones.

        Args:
            keyword: Search text.

        Returns:
            List of matching Record objects.
        """
        keyword_lower = keyword.lower()
        found_contacts = []

        for record in self.data.values():
            name_value = getattr(record.name, "value", "")
            if isinstance(name_value, str) and keyword_lower in name_value.lower():
                found_contacts.append(record)
                continue
            
            if record.email and isinstance(record.email.value, str) and keyword_lower in record.email.value.lower():
                found_contacts.append(record)
                continue

            if record.address and isinstance(record.address.value, str) and keyword_lower in record.address.value.lower():
                found_contacts.append(record)
                continue

            if record.birthday and keyword_lower in str(record.birthday):
                found_contacts.append(record)
                continue

            if any(isinstance(p.value, str) and keyword_lower in p.value.lower() for p in record.phones):
                found_contacts.append(record)
                continue
            
        return found_contacts
