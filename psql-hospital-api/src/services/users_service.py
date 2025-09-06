def validate_user(user_type, payload):
    fields_required = {
        'doctor': ['license', 'start_date', 'due_date', 'salary', 'name', 'email', 'phone', 'username', 'password'],
        'nurse': ['hierarchy', 'start_date', 'due_date', 'salary', 'name', 'email', 'phone', 'username', 'password'],
        'patient': ['name', 'email', 'phone', 'username', 'password'],
        'assistant': ['start_date', 'due_date', 'salary', 'name', 'email', 'phone', 'username', 'password']
    }
    missing_fields = [field for field in fields_required[user_type] if field not in payload]
    if missing_fields:
        return False, f'Missing fields: {", ".join(missing_fields)}'
    return True, None