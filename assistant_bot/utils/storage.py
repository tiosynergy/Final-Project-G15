from __future__ import annotations

import pickle
from pathlib import Path

from assistant_bot.models.address_book import AddressBook
from assistant_bot.models.notes import NotesManager


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATA_FILE = BASE_DIR / "data" / "addressbook.pkl"
DEFAULT_NOTES_FILE = BASE_DIR / "data" / "notes.pkl"


def _resolve_storage_path(filename: str | Path | None = None) -> Path:
    if filename is None:
        return DEFAULT_DATA_FILE

    path = Path(filename)
    if path.is_absolute():
        return path

    return BASE_DIR / path


def save_data(book: AddressBook, filename: str | Path | None = None) -> None:
    file_path = _resolve_storage_path(filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as file:
        pickle.dump(book, file)


def load_data(filename: str | Path | None = None) -> AddressBook:
    file_path = _resolve_storage_path(filename)
    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except (
        FileNotFoundError,
        EOFError,
        pickle.UnpicklingError,
        AttributeError,
        ModuleNotFoundError,
    ):
        return AddressBook()


def save_notes(notes: NotesManager, filename: str | Path | None = None) -> None:
    file_path = _resolve_storage_path(filename or DEFAULT_NOTES_FILE)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as file:
        pickle.dump(notes, file)


def load_notes(filename: str | Path | None = None) -> NotesManager:
    file_path = _resolve_storage_path(filename or DEFAULT_NOTES_FILE)
    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return NotesManager()
