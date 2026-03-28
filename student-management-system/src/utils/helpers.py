def generate_unique_id():
    import uuid
    return str(uuid.uuid4())

def format_date(date):
    return date.strftime("%Y-%m-%d")

def calculate_average(grades):
    if not grades:
        return 0
    return sum(grades) / len(grades)

def is_valid_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None