import re
def validate_email(email) -> bool:
    # Basic email validation pattern (does not allow consecutive dots or other special rules)
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    
    # Check basic email format using regex
    if not re.match(pattern, email):
        return False
    
    # Additional checks as per your requirements
    if "+" in email:
        return False  
    if email.count(".") > 1:  # Modify this rule if you want to allow more dots in specific places
        return False
    
    return True
