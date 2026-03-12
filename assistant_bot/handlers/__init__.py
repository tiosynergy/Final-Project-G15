from .commands import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    birthdays,
    change_contact,
    show_all,
    show_birthday,
    show_phone,
)
from .notes_commands import (
    add_note,
    delete_note,
    edit_note,
    search_notes,
    show_note,
    show_notes,
)

__all__ = [
    "add_contact",
    "change_contact",
    "show_phone",
    "show_all",
    "add_birthday",
    "show_birthday",
    "birthdays",
    "add_address",
    "add_email",
    "add_note",
    "edit_note",
    "delete_note",
    "show_note",
    "show_notes",
    "search_notes",
]
