# CLI Assistant Bot

Command-line assistant for managing contacts and text notes with persistent storage.

The application allows users to manage an address book, track upcoming birthdays, and store text notes directly from the terminal. The project is designed with a modular architecture suitable for collaborative development.

---

# Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Available Commands](#available-commands)
- [Usage Examples](#usage-examples)
- [Notes System](#notes-system)
- [Data Persistence](#data-persistence)
- [Error Handling](#error-handling)
- [Corner Case Handling](#corner-case-handling)
- [CLI Color Output](#cli-color-output)
- [Exit Commands](#exit-commands)

---

# Overview

CLI Assistant Bot is a terminal-based application that helps manage:

- contacts
- phone numbers
- email addresses
- physical addresses
- birthdays
- text notes

The program stores all data locally and restores it automatically when the application starts.

The architecture follows separation of concerns principles, making the code easy to maintain and extend.

---

# Features

## Contact Management

The assistant bot supports:

- adding new contacts
- updating phone numbers
- storing multiple phone numbers per contact
- adding email and address
- storing birthdays
- displaying upcoming birthdays

## Notes Management

The application also supports a text notes system:

- create notes
- edit notes
- delete notes
- search notes by keyword
- display a single note
- display all notes

---

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

- `models/`: domain entities and validation logic (`Field`, `Phone`, `Email`, `Record`, `AddressBook`, `Note`, `NotesManager`).
- `services/`: business logic independent from CLI and storage (`get_upcoming_birthdays`, notes keyword search).
- `handlers/`: command handlers used by CLI dispatcher for contacts and notes.
- `utils/`: shared utilities (`input_error`, parser, pickle storage).
- `main.py`: entry point and command dispatcher.

# Installation

Clone the repository:

```bash
git clone <repository_url>
cd <repository_folder>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure Python 3.9.6 or newer is installed.

## Running the Application

From the project root:

```bash
python -m assistant_bot.main
```

After starting the application you will see:

```text
Welcome to the assistant bot!
Enter a command:
```

## Available commands

### Contact Management

| Command                                      | Description                                                                   |
| :------------------------------------------- | :---------------------------------------------------------------------------- |
| `add <name> <phone>`                         | Create a new contact with a phone number (duplicate phone detection included) |
| `change-name <name> <old_phone> <new_phone>` | Replace an existing phone number                                              |
| `phone <name>`                               | Display all phone numbers of a contact                                        |
| `all`                                        | Display all saved contacts                                                    |
| `add-birthday <name> <DD.MM.YYYY>`           | Add a birthday to a contact                                                   |
| `show-birthday <name>`                       | Show the birthday of a contact                                                |
| `add-address <name> <address>`               | Add an address to a contact                                                   |
| `change-address <name> <address>`            | Update the address of a contact                                               |
| `add-email <name> <email>`                   | Add an email to a contact                                                     |
| `change-email <name> <email>`                | Update the email of a contact                                                 |
| `birthdays` <n>                              | Display upcoming birthdays for n days                                         |

---

### Notes Management

| Command                  | Description             |
| :----------------------- | :---------------------- |
| `add-note <text>`        | Create a new note       |
| `edit-note <id> <text>`  | Edit an existing note   |
| `delete-note <id>`       | Delete a note           |
| `show-note <id>`         | Display a specific note |
| `show-notes`             | Display all saved notes |
| `search-notes <keyword>` | Search notes by keyword |

---

### Application Management

| Command           | Description                                               |
| :---------------- | :-------------------------------------------------------- |
| `hello`           | Display greeting message                                  |
| `help`            | Display all available commands with usage and description |
| `exit` or `close` | Save data and close the application                       |

## Usage Examples

### Adding a contact

```bash
add John 0501234567
```

**Output**

```
Contact added.
```

---

### Updating a phone number

```bash
change John 0501234567 0995554444
```

**Output**

```
Phone for John changed from 0501234567 to 0995554444
```

---

### Adding a birthday

```bash
add-birthday John 15.03.1995
```

**Output**

```
Birthday for John added: 15.03.1995
```

---

### Creating a note

```bash
add-note Buy milk and bread tomorrow
```

**Output**

```
Note added with id 1.
```

---

### Searching notes

```bash
search-notes milk
```

**Output**

```
[1] Buy milk and bread tomorrow
```

## Notes System

Each note contains:

- unique identifier
- note text
- creation timestamp
- last modification timestamp

### Example output

```text

[1] Created: 2026-03-11 18:42
Buy milk and bread
```

---

## Note Length Limit

To prevent extremely large CLI input and ensure stable performance, the note length is limited.

Recommended limit:

```text
5000 characters
```

If the limit is exceeded the program returns:

```text
Note is too long. Maximum length is 5000 characters.
```

---

## Data Persistence

All data is stored locally using pickle serialization.

Files used by the application:

| File                   | Description     |
| ---------------------- | --------------- |
| `data/addressbook.pkl` | Stores contacts |
| `data/notes.pkl`       | Stores notes    |

Data is automatically:

- loaded when the program starts
- saved when the program exits

---

## Error Handling

The application uses a centralized error handling decorator.

Handled errors include:

| Error Type      | Example                      |
| --------------- | ---------------------------- |
| Invalid phone   | phone must contain 10 digits |
| Invalid email   | incorrect email format       |
| Invalid date    | birthday format error        |
| Missing contact | contact not found            |
| Missing note    | note ID not found            |

### Example

```bash
add John 123
```

Output:

```text
Phone number must be 10 digits.
```

---

## Corner Case Handling

### Leap Year Birthdays

If a birthday is February 29 and the current year is not a leap year, the birthday is shifted to February 28.

### Weekend Birthdays

If a birthday falls on a weekend:

| Day      | Congratulation moved to |
| -------- | ----------------------- |
| Saturday | Monday                  |
| Sunday   | Monday                  |

### Empty Address

If an empty address is provided:

```text
Address cannot be empty.
```

### Missing Phone Numbers

If a contact exists but has no phone numbers:

```text
John has no phones.
```

---

## CLI Color Output

The application uses colored terminal output for better readability.

| Color  | Purpose                                                   |
| ------ | --------------------------------------------------------- |
| Yellow | Welcome and Good bye messages                             |
| Blue   | Enter a command prompt and command names in `help` output |
| Green  | Contact names and notes id in output                      |

---

## Duplicate Phone Detection

When adding a phone number to an existing contact, the bot checks whether the phone is already recorded.

Example — contact `Tata` already has phone `1234567890`:

```bash
add Tata 1234567890
```

**Output**

```text
Phone 1234567890 is already recorded for Tata.
```

The contact is not modified, and no duplicate entry is created.

---

## Help Command

Displays all available commands grouped by category, with usage syntax and a brief description.

```bash
help
```

**Output**

```text
Available commands:

Contacts:
  add <name> <phone>                                     Create a new contact or add a phone to existing
  change <name> <old_phone> <new_phone>                  Update a phone number of a contact
  delete <name>                                          Delete an existing contact
  search <keyword>                                       Find a record by keyword
  delete-phone <name> <phone>                            Delete the phone number of a contact
  phone <name>                                           Show all phone numbers of a contact
  change-name <old_name> <new_name>                      Update contact name
  add-birthday <name> <DD.MM.YYYY>                       Add a birthday to a contact
  change-birthday <name> <old_birthday> <new_birthday>   Replace an existing birthday (date format: DD.MM.YYYY)
  show-birthday <name>                                   Show the birthday of a contact
  birthdays <number_of_days>                             Shows birthdays in specified amount of days
  add-address <name> <address>                           Add an address of a contact
  change-address <name> <address>                        Update the address of a contact
  delete-address <name>                                  Delete the address of a contact
  add-email <name> <email>                               Add an email to a contact
  change-email <name> <email>                            Update the email of a contact
  delete-email <name> <email>                            Delete the email of a contact
  all                                                    Show all saved contacts

Notes:
  add-note <text>                                        Create a new note
  edit-note <id> <text>                                  Edit an existing note
  delete-note <id>                                       Delete a note
  show-note <id>                                         Display a specific note
  show-notes                                             Display all saved notes
  search-notes <keyword>                                 Search notes by keyword

General:
  hello                                                  Display greeting message
  help                                                   Show this help message
  exit / close                                           Save data and close the application
```

Command names are highlighted in cyan, section headers in yellow.

---

## Exit Commands

To safely exit the program and save data:

```bash
exit
```

or

```bash
close
```

Output:

```text
Good bye!
```
