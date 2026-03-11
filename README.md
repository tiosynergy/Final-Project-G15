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
│   └── address_book.py
├── services/
│   ├── __init__.py
│   └── birthday_service.py
├── handlers/
│   ├── __init__.py
│   └── commands.py
└── utils/
	├── __init__.py
	├── decorators.py
	├── parser.py
	└── storage.py

data/
└── addressbook.pkl

README.md
```

## Architecture overview

- `models/`: Domain entities and validation logic (`Field`, `Phone`, `Email`, `Record`, `AddressBook`, etc.).
- `services/`: Business logic independent from CLI and storage (`get_upcoming_birthdays`).
- `handlers/`: Command handlers used by CLI dispatcher.
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
- `close` or `exit`

## Data persistence

Contacts are stored in `data/addressbook.pkl` using `pickle`.

## Notes

- Main entry point for the app is `assistant_bot/main.py`.
