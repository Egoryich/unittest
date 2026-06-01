def _require_str(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("value must be str")
    return value.strip()


def parse_port(value: str) -> int:
    stripped = _require_str(value)
    if not stripped.isdigit():
        raise ValueError("port must contain only digits")
    port = int(stripped)
    if not 1 <= port <= 65535:
        raise ValueError("port must be in range 1..65535")
    return port


def parse_bool(value: str) -> bool:
    stripped = _require_str(value).lower()
    true_values = {"1", "true", "yes", "on"}
    false_values = {"0", "false", "no", "off"}
    if stripped in true_values:
        return True
    if stripped in false_values:
        return False
    raise ValueError("bool must be one of 1/0 true/false yes/no on/off")


def parse_csv(value: str) -> list[str]:
    stripped = _require_str(value)
    return [item.strip() for item in stripped.split(",") if item.strip()]

