from __future__ import annotations

from collections import UserDict

from .record import Record


class AddressBook(UserDict[str, Record]):
    def add_record(self, record: Record) -> None:
        self.data[str(record.name.value)] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        self.data.pop(name, None)

    def change_record_name(self, old_name: str, new_name: str) -> None:
        if old_name not in self.data:
            raise KeyError(f"Contact {old_name} not found.")
        
        record = self.data.pop(old_name)

        record.edit_name(new_name)

        self.data[new_name] = record

    def search_contacts(self, keyword: str) -> list:
        keyword_lower = keyword.lower()
        found_contacts = []

        for record in self.data.values():
            if keyword_lower in record.name.value.lower():
                found_contacts.append(record)
                continue
            
            if record.email and keyword_lower in record.email.value.lower():
                found_contacts.append(record)
                continue

            if record.address and keyword_lower in record.address.value.lower():
                found_contacts.append(record)
                continue

            if record.birthday and keyword_lower in record.birthday.value.lower():
                found_contacts.append(record)
                continue

            if any(keyword_lower in p.value.lower() for p in record.phones):
                found_contacts.append(record)
                continue
        return found_contacts