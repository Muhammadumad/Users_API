USERS = {}


def normalize_email(email):
    return email.strip().lower()


def email_in_use(email, exclude_user_id=None):
    normalized_email = normalize_email(email)
    for user_id, user in USERS.items():
        if exclude_user_id is not None and user_id == exclude_user_id:
            continue
        if normalize_email(user['email']) == normalized_email:
            return True
    return False