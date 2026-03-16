from __future__ import annotations

from datetime import datetime

from assistant_bot.models.address_book import AddressBook

def get_upcoming_birthdays(number_of_days: str, book: AddressBook) -> list[dict[str, str]]:
    """Collect contacts with birthdays in the next N days.

    Args:
        number_of_days: Number of upcoming days as a string.
        book: Address book storage.

    Returns:
        A list of dictionaries with keys "name" and "congratulation_date".

    Errors:
        ValueError can be raised if number_of_days cannot be converted to int.
    """
    days_int = int(number_of_days)
    today = datetime.today().date()
    upcoming_birthdays = []

    for record in book.data.values():
        if record.birthday:
            b_date = record.birthday.value
            
            try:
                b_date_this_year = b_date.replace(year=today.year)
            except ValueError:
                b_date_this_year = b_date.replace(year=today.year, month=3, day=1)
            
            if b_date_this_year < today:
                try:
                    b_date_this_year = b_date.replace(year=today.year + 1)
                except ValueError:
                    b_date_this_year = b_date.replace(year=today.year + 1, month=3, day=1)
            
            delta_days = (b_date_this_year - today).days
            
            if 0 <= delta_days <= days_int:
                congratulation_date = b_date_this_year.strftime("%d.%m.%Y")
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date
                })
                
    return upcoming_birthdays
