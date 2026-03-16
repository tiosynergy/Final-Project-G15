from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any


def input_error(func: Callable[..., str]) -> Callable[..., str]:
    """Wrap command handlers and map exceptions to user-friendly messages.

    Args:
        func: Command handler function returning a string response.

    Returns:
        Wrapped handler that catches expected exceptions and returns readable text.

    Errors:
        ValueError, IndexError, and KeyError are handled and transformed.
        Unexpected exceptions are returned as "Error: ...".
    """
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> str:
        """Execute wrapped handler with standardized error mapping.

        Args:
            *args: Positional arguments for wrapped function.
            **kwargs: Keyword arguments for wrapped function.

        Returns:
            Handler result or mapped error message.
        """
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError) as error:
            message = str(error)
            if "10" in message:
                return "Phone number must be 10 digits."
            
            if "Invalid date format" in message:
                return "Invalid date format. Use DD.MM.YYYY"
            
            if "Invalid email format" in message:
                return "Invalid email format. Use example@domain.com"
            
            if "Address cannot be empty" in message:
                return "Address cannot be empty."
            
            if "Note" in message or "note" in message:
                return message
            
            if "Keyword cannot be empty" in message:
                return message
            
            if "not found" in message.lower():
                return "Contact or phone not found."
            
            return "Give me name and correct data please."
        
        except Exception as error:
            return f"Error: {str(error)}"

    return inner
