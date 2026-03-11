# Final-Project-G15

CLI assistant bot with a modular clean architecture.

## Project structure

```text
assistant_bot/
├── __init__.py
├── main.py
├── models/
│   ├── __init__.py
│   ├── fields.py
│   ├── record.py
│   ├── address_book.py
│   └── notes.py
├── services/
│   ├── __init__.py
│   ├── birthday_service.py
│   └── search_service.py
├── handlers/
│   ├── __init__.py
│   ├── commands.py
│   └── notes_commands.py
└── utils/
    ├── __init__.py
    ├── decorators.py
    ├── parser.py
    └── storage.py

data/
├── addressbook.pkl
└── notes.pkl

README.md
```

## Architecture overview

- `models/`: Domain entities and validation logic (`Field`, `Phone`, `Email`, `Record`, `AddressBook`, `Note`, `NotesManager`).
- `services/`: Business logic independent from CLI and storage (`get_upcoming_birthdays`, notes keyword search).
- `handlers/`: Command handlers used by CLI dispatcher for contacts and notes.
- `utils/`: Cross-cutting helpers (`input_error`, parser, pickle storage).
- `main.py`: CLI loop and command router.

## Run

From the project root:

```bash
python -m assistant_bot.main
```

## Supported commands

- `hello`
- `add <name> <phone>`
- `change <name> <old_phone> <new_phone>`
- `phone <name>`
- `all`
- `add-birthday <name> <DD.MM.YYYY>`
- `show-birthday <name>`
- `add-address <name> <address>`
- `add-email <name> <email>`
- `birthdays`
- `add-note <text...>`
- `edit-note <id> <new_text...>`
- `delete-note <id>`
- `show-note <id>`
- `show-notes`
- `search-notes <keyword...>`
- `close` or `exit`

## Data persistence

Contacts are stored in `data/addressbook.pkl` using `pickle`.
Notes are stored in `data/notes.pkl` using `pickle`.

## Notes

- Main entry point for the app is `assistant_bot/main.py`.
