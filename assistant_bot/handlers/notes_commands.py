from __future__ import annotations

from assistant_bot.models.notes import NotesManager
from assistant_bot.services.search_service import search_notes_by_keyword
from assistant_bot.utils.decorators import input_error


def _parse_note_id(raw_id: str) -> int:
    if not raw_id.isdigit():
        raise ValueError("Note id must be a positive integer.")
    note_id = int(raw_id)
    if note_id <= 0:
        raise ValueError("Note id must be a positive integer.")
    return note_id


def _format_note(note_id: int, text: str, status_label: str, status_time: str) -> str:
    return f"[{note_id}] {status_label}: {status_time}\n{text}"


@input_error
def add_note(args: list[str], manager: NotesManager) -> str:
    text = " ".join(args).strip()
    note = manager.add_note(text)
    return f"Note added with id {note.id}."


@input_error
def edit_note(args: list[str], manager: NotesManager) -> str:
    note_id_raw, *text_parts = args
    note_id = _parse_note_id(note_id_raw)
    new_text = " ".join(text_parts).strip()
    manager.edit_note(note_id, new_text)
    return f"Note {note_id} updated."


@input_error
def delete_note(args: list[str], manager: NotesManager) -> str:
    note_id_raw, *_ = args
    note_id = _parse_note_id(note_id_raw)
    manager.delete_note(note_id)
    return f"Note {note_id} deleted."


@input_error
def show_note(args: list[str], manager: NotesManager) -> str:
    note_id_raw, *_ = args
    note_id = _parse_note_id(note_id_raw)
    note = manager.find_note(note_id)
    if note is None:
        return f"Note with id {note_id} not found."

    return _format_note(
        note.id,
        note.text,
        note.get_status_label(),
        note.get_status_time().strftime("%d.%m.%Y %H:%M:%S"),
    )


@input_error
def show_notes(_: list[str], manager: NotesManager) -> str:
    notes = manager.get_all_notes()
    if not notes:
        return "No notes yet."

    lines: list[str] = []
    for note in notes:
        lines.append(
            _format_note(
                note.id,
                note.text,
                note.get_status_label(),
                note.get_status_time().strftime("%d.%m.%Y %H:%M:%S"),
            )
        )

    return "\n\n".join(lines)


@input_error
def search_notes(args: list[str], manager: NotesManager) -> str:
    keyword = " ".join(args).strip()
    if not keyword:
        raise ValueError("Keyword cannot be empty.")

    matched_notes = search_notes_by_keyword(manager, keyword)
    if not matched_notes:
        return "No matching notes found."

    return "\n\n".join(
        _format_note(
            note.id,
            note.text,
            note.get_status_label(),
            note.get_status_time().strftime("%d.%m.%Y %H:%M:%S"),
        )
        for note in matched_notes
    )
