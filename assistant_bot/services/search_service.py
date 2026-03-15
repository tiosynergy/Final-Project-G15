from __future__ import annotations

from assistant_bot.models.notes import Note, NotesManager
from assistant_bot.models.record import Record
from assistant_bot.models.address_book import AddressBook


def search_notes_by_keyword(manager: NotesManager, keyword: str) -> list[Note]:
    """Return notes that contain a keyword.

    Args:
        manager: Notes storage manager.
        keyword: Search text.

    Returns:
        List of matched notes.
    """
    return manager.search_notes(keyword)

def search_contacts_by_keyword(book: AddressBook, keyword: str) -> list[Record]:
    """Return contacts that contain a keyword in any searchable field.

    Args:
        book: Address book storage.
        keyword: Search text.

    Returns:
        List of matched contact records.
    """
    return book.search_contacts(keyword)

