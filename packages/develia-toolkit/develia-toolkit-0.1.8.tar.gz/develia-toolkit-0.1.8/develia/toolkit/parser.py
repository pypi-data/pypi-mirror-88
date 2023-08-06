import typing as _typing


def parse_float(string: str,
                decimal_separator=".",
                fallback=None) -> _typing.Any:
    try:
        if decimal_separator != ".":
            string = string.replace(decimal_separator, ".")
        return float(string)

    except ValueError:
        return fallback() if callable(fallback) else fallback
