from __future__ import annotations


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Parse raw CLI input into a command and argument list.

    Args:
        user_input: Raw user-entered command line.

    Returns:
        Tuple of lowercased command and list of arguments.
    """
    parts = user_input.strip().split()
    if not parts:
        return "", []
    
    command = parts[0].lower()
    args = parts[1:]
    
    return command, args
