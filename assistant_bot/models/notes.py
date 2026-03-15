from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


MAX_NOTE_LENGTH = 5000


@dataclass
class Note:
    """Single note entity with metadata about status and update time."""

    id: int
    text: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: str = "Created"

    def __post_init__(self) -> None:
        """Validate initial note state after dataclass initialization."""
        self._validate_text(self.text)
        if self.status not in {"Created", "Updated"}:
            self.status = "Created"

    @staticmethod
    def _validate_text(text: str) -> None:
        """Validate note text constraints.

        Args:
            text: Note content text.

        Errors:
            Raises ValueError when text is empty or exceeds maximum length.
        """
        if not text.strip():
            raise ValueError("Note text cannot be empty.")
        
        if len(text) > MAX_NOTE_LENGTH:
            raise ValueError(
                f"Note text exceeds maximum length of {MAX_NOTE_LENGTH} characters."
            )

    def update_text(self, new_text: str) -> None:
        """Update note content and refresh metadata.

        Args:
            new_text: New note text.

        Errors:
            Raises ValueError when text validation fails.
        """
        self._validate_text(new_text)
        self.text = new_text
        self.timestamp = datetime.now()
        self.status = "Updated"

    def get_status_label(self) -> str:
        """Get a status label with backward compatibility for old serialized notes.

        Returns:
            "Created" or "Updated" status label.
        """
        if hasattr(self, "status") and self.status in {"Created", "Updated"}:
            return self.status

        # Backward compatibility for already saved notes with old fields.
        created_at = getattr(self, "created_at", None)
        updated_at = getattr(self, "updated_at", None)
        if created_at is not None and updated_at is not None:
            return "Updated" if updated_at != created_at else "Created"

        return "Created"

    def get_status_time(self) -> datetime:
        """Get status-related timestamp with backward compatibility.

        Returns:
            Datetime of current status event.
        """
        if hasattr(self, "timestamp"):
            return self.timestamp

        created_at = getattr(self, "created_at", None)
        updated_at = getattr(self, "updated_at", None)
        if created_at is not None and updated_at is not None:
            return updated_at if updated_at != created_at else created_at

        return datetime.now()


class NotesManager:
    """In-memory manager for CRUD and search operations on notes."""

    def __init__(self) -> None:
        """Initialize an empty notes collection and id counter."""
        self._notes: dict[int, Note] = {}
        self._next_id: int = 1

    def add_note(self, text: str) -> Note:
        """Create and store a new note.

        Args:
            text: Note content.

        Returns:
            Newly created Note object.

        Errors:
            Raises ValueError if note text validation fails.
        """
        note = Note(id=self._next_id, text=text)
        self._notes[note.id] = note
        self._next_id += 1

        return note

    def edit_note(self, note_id: int, new_text: str) -> Note:
        """Edit an existing note by id.

        Args:
            note_id: Target note id.
            new_text: Replacement note text.

        Returns:
            Updated Note object.

        Errors:
            Raises ValueError if note is not found or new text is invalid.
        """
        note = self.find_note(note_id)
        if note is None:
            raise ValueError(f"Note with id {note_id} not found.")
        
        note.update_text(new_text)
        
        return note

    def delete_note(self, note_id: int) -> None:
        """Delete a note by id.

        Args:
            note_id: Target note id.

        Errors:
            Raises ValueError if note id is not found.
        """
        if note_id not in self._notes:
            raise ValueError(f"Note with id {note_id} not found.")
        
        del self._notes[note_id]

    def find_note(self, note_id: int) -> Note | None:
        """Find a note by id.

        Args:
            note_id: Target note id.

        Returns:
            Matching Note or None.
        """
        return self._notes.get(note_id)

    def search_notes(self, keyword: str) -> list[Note]:
        """Search notes by keyword in note text.

        Args:
            keyword: Search text.

        Returns:
            List of matched notes.
        """
        normalized_keyword = keyword.lower().strip()
        return [
            note
            for note in self._notes.values()
            if normalized_keyword in note.text.lower()
        ]

    def get_all_notes(self) -> list[Note]:
        """Return all notes sorted by id.

        Returns:
            Sorted list of Note objects.
        """
        return sorted(self._notes.values(), key=lambda note: note.id)
