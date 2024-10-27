import re

def validate_password(password) -> bool:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d|\W).{6,}$"
    return bool(re.match(pattern, password))
