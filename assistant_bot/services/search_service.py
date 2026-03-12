from __future__ import annotations

from assistant_bot.models.notes import Note, NotesManager


def search_notes_by_keyword(manager: NotesManager, keyword: str) -> list[Note]:
    """Return notes that contain the keyword (case-insensitive)."""
    return manager.search_notes(keyword)
