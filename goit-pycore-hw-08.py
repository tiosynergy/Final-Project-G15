from collections import UserDict
from datetime import datetime, date, timedelta
import pickle

# Класи 
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
    #  перевірка на правильність наведених значень та
    #  виклик Декоратора обробки помилок вводу
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("10")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value: str):
    # перевірка на правильність наведених значень та 
    # виклик Декоратора обробки помилок вводу    
        try:
            dt = datetime.strptime(value, "%d.%m.%Y")
            self.value = dt.date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
    # Додане поле birthday для дня народження в клас Record, клас Birthday
        self.birthday: Birthday | None = None

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        for i, phone in enumerate(self.phones):
            if phone.value == phone_number:
                self.phones.pop(i)
                return
        raise ValueError(f"Phone {phone_number} not found")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone_number: str) -> Phone | None:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
# -- додано add_birthday, яка додає день народження до контакту.
    def add_birthday(self, birthday_str: str) -> None:
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "no phones"
        bday = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{bday}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        self.data.pop(name, None)

# -------- Адаптована функція get_upcoming_birthdays з 3-го ДЗ
#  Початок функції кого з колег потрібно привітати ----
    def get_upcoming_birthdays(self):
        """Повертає список словників з контактами, яких потрібно привітати протягом наступних 7 днів"""
        now = datetime.now().date()   # поточна дата

        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            # приведення дати народження до об'єкта date
            birthday = record.birthday.value   # вже date з класу Birthday

            # визначення дня народження в поточному році
            try:
                birthday_this_year = datetime(now.year, birthday.month, birthday.day).date()
            except ValueError:
            # 29 Лютого в невисокосному році переносима на 28 Лютого
                birthday_this_year = datetime(now.year, birthday.month, birthday.day - 1).date()

            user_birthday_this_year = {
            "name": record.name.value,
            "birthday": birthday_this_year
            }

            # перевірка чи ДР вже минув у цьому році
            if user_birthday_this_year["birthday"] < now:
                # print(f"\nДень народження {user_birthday_this_year['name']} в цьому році минув")  # закоментуй якщо не потрібно
                user_birthday_next_year = {
                    "name": record.name.value,
                    "birthday": datetime(now.year + 1, birthday.month, birthday.day).date()
                }
                # print(f"Наступний день народження {user_birthday_next_year['birthday']}")  # закоментуй

                congratulation_date = user_birthday_next_year

                # Якщо наступний ДР у суботу → +2 дні
                if congratulation_date["birthday"].weekday() == 5:
                    new_date = congratulation_date["birthday"] + timedelta(days=2)
                    congratulation_date = {
                        "name": record.name.value,
                        "birthday": new_date,
                        "r_b": birthday   # оригінальна дата народження
                    }
                    # print(f"Привітання {congratulation_date['birthday']}\n")  # закоментуй

                # Якщо наступний ДР у неділю → +1 день
                elif congratulation_date["birthday"].weekday() == 6:
                    new_date = congratulation_date["birthday"] + timedelta(days=1)
                    congratulation_date = {
                        "name": record.name.value,
                        "birthday": new_date,
                        "r_b": birthday
                    }
                    # print(f"Привітання {congratulation_date['birthday']}\n")  # закоментуй

            else:
                congratulation_date = user_birthday_this_year
                congratulation_date["r_b"] = birthday

            # визначення чи потрапляє в наступні 7 днів
            if 0 <= (congratulation_date["birthday"] - now).days <= 7:

                # якщо ДР припадає на суботу +2 дні
                if congratulation_date["birthday"].weekday() == 5:
                    new_date = congratulation_date["birthday"] + timedelta(days=2)
                    congratulation_date = {
                        "name": record.name.value,
                        "birthday": new_date,
                        "r_b": birthday
                    }

                # якщо ДР припадає на неділю +1 день
                if congratulation_date["birthday"].weekday() == 6:
                    new_date = congratulation_date["birthday"] + timedelta(days=1)
                    congratulation_date = {
                        "name": record.name.value,
                        "birthday": new_date,
                        "r_b": birthday
                    }

                upcoming_birthdays.append(congratulation_date)

        return upcoming_birthdays

#--- Декоратор обробки помилок вводу

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError) as e:
            if "10" in str(e):
                return "Phone number must be 10 digits."
            if "Invalid date format" in str(e):
                return "Invalid date format. Use DD.MM.YYYY"
            if "not found" in str(e).lower():
                return "Contact or phone not found."
            return "Give me name and correct data please."
        except Exception as e:
            return f"Error: {str(e)}"
    return inner


# додано функції-обробники

@input_error
def add_contact(args, book: AddressBook):
    """додавання нового контакту або оновлення телефону для контакту,
    що вже існує в адресній книзі"""
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        msg = "Contact added."
    else:
        msg = "Contact updated."

    if phone:
        record.add_phone(phone)

    return msg


@input_error
def change_contact(args, book: AddressBook):
    """Змінити телефонний номер для вказаного контакту."""
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    record.edit_phone(old_phone, new_phone)
    return f"Phone for {name} changed from {old_phone} to {new_phone}."


@input_error
def show_phone(args, book: AddressBook):
    """показуємо день народження контакту"""
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    if not record.phones:
        return f"{name} has no phones."
    return f"{name}'s phones: {', '.join(p.value for p in record.phones)}"


@input_error
def show_all(_, book: AddressBook):
    """Показати всі контакти в адресній книзі."""
    if not book.data:
        return "No contacts yet."
    lines = [str(record) for record in book.data.values()]
    return "\n".join(lines)


@input_error
def add_birthday(args, book: AddressBook):
    """Додати дату народження для вказаного контакту."""
    name, date_str, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found")
    #     return f"Contact {name} not found."
    record.add_birthday(date_str)
    return f"Birthday for {name} aded: {date_str}"


@input_error
def show_birthday(args, book: AddressBook):
    """Показати дату народження для вказаного контакту"""
    name, *_ = args
    record = book.find(name)
    return f"День Народення {name} : {record.birthday}"


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "На цьому тижні немає днів народження для привітання."
    birthday = ["Список привітань на цьому тижні:\n"]
    for bd in upcoming:
        birthday.append(
            f"{bd['name']}, день народження {bd['r_b'].strftime('%Y.%m.%d')} : "
            f"привітати {bd['birthday'].strftime('%d.%m.%Y')}"
        )
    return "\n".join(birthday)


#---- прибирамо помилки при введенні 

def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return AddressBook()  # якщо файл відсутній або пошкоджений — нова книга

# -------- Головний функціонал

def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()