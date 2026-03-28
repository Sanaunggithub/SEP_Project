def is_valid_email(email):
    import re
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_required_field_filled(field_value):
    return bool(field_value and field_value.strip())

def validate_student_data(student_data):
    errors = {}
    
    if not is_required_field_filled(student_data.get('name')):
        errors['name'] = 'Name is required.'
    
    if not is_valid_email(student_data.get('email')):
        errors['email'] = 'Invalid email format.'
    
    if not is_required_field_filled(student_data.get('courses')):
        errors['courses'] = 'At least one course is required.'
    
    return errors if errors else None