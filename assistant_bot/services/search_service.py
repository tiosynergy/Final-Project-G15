from __future__ import annotations

from assistant_bot.models.notes import Note, NotesManager
from assistant_bot.models.record import Record
from assistant_bot.models.address_book import AddressBook


def search_notes_by_keyword(manager: NotesManager, keyword: str) -> list[Note]:
    """Return notes that contain the keyword (case-insensitive)."""
    return manager.search_notes(keyword)

def search_contacts_by_keyword(book: AddressBook, keyword: str) -> list[Record]
    """Return contacts that contain the keywor in any field(case-insensitive)."""
    return book.search_contacts(keyword)

