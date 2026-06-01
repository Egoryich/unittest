def parse_port(value):
    """Convert value to a TCP/UDP port and validate the 1..65535 range."""
    if isinstance(value, bool):
        raise TypeError("port must be int or str")

    if isinstance(value, int):
        port = value
    elif isinstance(value, str):
        stripped = value.strip()
        if not stripped.isdigit():
            raise ValueError("port must contain only digits")
        port = int(stripped)
    else:
        raise TypeError("port must be int or str")

    if not 1 <= port <= 65535:
        raise ValueError("port must be in range 1..65535")
    return port

