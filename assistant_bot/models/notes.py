from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


MAX_NOTE_LENGTH = 5000


@dataclass
class Note:
    id: int
    text: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "Created"

    def __post_init__(self) -> None:
        self._validate_text(self.text)
        if self.status not in {"Created", "Updated"}:
            self.status = "Created"

    @staticmethod
    def _validate_text(text: str) -> None:
        if not text.strip():
            raise ValueError("Note text cannot be empty.")
        
        if len(text) > MAX_NOTE_LENGTH:
            raise ValueError(
                f"Note text exceeds maximum length of {MAX_NOTE_LENGTH} characters."
            )

    def update_text(self, new_text: str) -> None:
        self._validate_text(new_text)
        self.text = new_text
        self.timestamp = datetime.now()
        self.status = "Updated"

    def get_status_label(self) -> str:
        if hasattr(self, "status") and self.status in {"Created", "Updated"}:
            return self.status

        # Backward compatibility for already saved notes with old fields.
        created_at = getattr(self, "created_at", None)
        updated_at = getattr(self, "updated_at", None)
        if created_at is not None and updated_at is not None:
            return "Updated" if updated_at != created_at else "Created"

        return "Created"

    def get_status_time(self) -> datetime:
        if hasattr(self, "timestamp"):
            return self.timestamp

        created_at = getattr(self, "created_at", None)
        updated_at = getattr(self, "updated_at", None)
        if created_at is not None and updated_at is not None:
            return updated_at if updated_at != created_at else created_at

        return datetime.now()


class NotesManager:
    def __init__(self) -> None:
        self._notes: dict[int, Note] = {}
        self._next_id: int = 1

    def add_note(self, text: str) -> Note:
        note = Note(id=self._next_id, text=text)
        self._notes[note.id] = note
        self._next_id += 1

        return note

    def edit_note(self, note_id: int, new_text: str) -> Note:
        note = self.find_note(note_id)
        if note is None:
            raise ValueError(f"Note with id {note_id} not found.")
        
        note.update_text(new_text)
        
        return note

    def delete_note(self, note_id: int) -> None:
        if note_id not in self._notes:
            raise ValueError(f"Note with id {note_id} not found.")
        
        del self._notes[note_id]

    def find_note(self, note_id: int) -> Note | None:
        return self._notes.get(note_id)

    def search_notes(self, keyword: str) -> list[Note]:
        normalized_keyword = keyword.lower().strip()
        return [
            note
            for note in self._notes.values()
            if normalized_keyword in note.text.lower()
        ]

    def get_all_notes(self) -> list[Note]:
        return sorted(self._notes.values(), key=lambda note: note.id)
