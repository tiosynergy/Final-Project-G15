from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from assistant_bot.models.address_book import AddressBook

def get_upcoming_birthdays(book: AddressBook) -> list[dict[str, Any]]:
    """Return contacts to congratulate in the next 7 days."""
    today = datetime.today().date()
    end_date = today + timedelta(days=7)

    upcoming_birthdays: list[dict[str, Any]] = []

    for record in book.data.values():
        if record.birthday is None:
            continue

        birthday = record.birthday.value

        try:
            birthday_this_year = birthday.replace(year=today.year)
        except ValueError:
            # Feb 29 birthday in non-leap year -> Feb 28.
            birthday_this_year = birthday.replace(year=today.year, day=28)

        if birthday_this_year < today:
            try:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            except ValueError:
                birthday_this_year = birthday.replace(year=today.year + 1, day=28)

        if today <= birthday_this_year <= end_date:
            congratulation_date = birthday_this_year

            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append(
                {
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                }
            )

    return upcoming_birthdays
