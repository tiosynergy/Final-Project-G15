from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from assistant_bot.models.address_book import AddressBook


def get_upcoming_birthdays(book: AddressBook) -> list[dict[str, Any]]:
    """Return contacts to congratulate in the next 7 days."""
    now = datetime.now().date()
    upcoming_birthdays: list[dict[str, Any]] = []

    for record in book.data.values():
        if record.birthday is None:
            continue

        birthday = record.birthday.value

        try:
            birthday_this_year = datetime(now.year, birthday.month, birthday.day).date()
        except ValueError:
            birthday_this_year = datetime(now.year, birthday.month, birthday.day - 1).date()

        user_birthday_this_year = {
            "name": record.name.value,
            "birthday": birthday_this_year,
        }

        if user_birthday_this_year["birthday"] < now:
            user_birthday_next_year = {
                "name": record.name.value,
                "birthday": datetime(now.year + 1, birthday.month, birthday.day).date(),
            }

            congratulation_date = user_birthday_next_year

            if congratulation_date["birthday"].weekday() == 5:
                new_date = congratulation_date["birthday"] + timedelta(days=2)
                congratulation_date = {
                    "name": record.name.value,
                    "birthday": new_date,
                    "r_b": birthday,
                }
            elif congratulation_date["birthday"].weekday() == 6:
                new_date = congratulation_date["birthday"] + timedelta(days=1)
                congratulation_date = {
                    "name": record.name.value,
                    "birthday": new_date,
                    "r_b": birthday,
                }
        else:
            congratulation_date = user_birthday_this_year
            congratulation_date["r_b"] = birthday

        if 0 <= (congratulation_date["birthday"] - now).days <= 7:
            if congratulation_date["birthday"].weekday() == 5:
                new_date = congratulation_date["birthday"] + timedelta(days=2)
                congratulation_date = {
                    "name": record.name.value,
                    "birthday": new_date,
                    "r_b": birthday,
                }

            if congratulation_date["birthday"].weekday() == 6:
                new_date = congratulation_date["birthday"] + timedelta(days=1)
                congratulation_date = {
                    "name": record.name.value,
                    "birthday": new_date,
                    "r_b": birthday,
                }

            upcoming_birthdays.append(congratulation_date)

    return upcoming_birthdays
