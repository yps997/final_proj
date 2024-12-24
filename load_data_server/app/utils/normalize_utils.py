def normalize_number(value):
    try:
        number = int(value)
        return number if number >= 0 else 0
    except (ValueError, TypeError):
        return 0