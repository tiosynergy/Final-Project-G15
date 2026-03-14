from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from assistant_bot.models.address_book import AddressBook

def get_upcoming_birthdays(number_of_days, book: AddressBook) -> list[dict[str, Any]]:
    """Return contacts to congratulate on the specified date."""
    target_date = datetime.today().date() + timedelta(days=int(number_of_days))

    upcoming_birthdays: list[dict[str, Any]] = []

    for record in book.data.values():
        if record.birthday:
            b_date = record.birthday.value
            try:
                b_date_target_year = b_date.replace(year=target_date.year)
            except ValueError:
            # Feb 29 birthday in non-leap year -> Feb 28.
                b_date_target_year = b_date.replace(year=target_date.year, day=28)

            if b_date_target_year == target_date:
                upcoming_birthdays.append(
                {
                    "name": record.name.value,
                    "congratulation_date": b_date_target_year.strftime("%d.%m.%Y"),
                }
            )

    return upcoming_birthdays
