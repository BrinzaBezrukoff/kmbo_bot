from functools import wraps

from models import get_user, get_db, close_db


def user_required(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        db = get_db()
        user = get_user(db, message.from_user.id)
        close_db()
        return func(message, *args, **kwargs, user=user)
    return wrapper


def role_required(role, error_cb):
    def role_required_decor(func):
        @wraps(func)
        def wrapper(message, *args, **kwargs):
            db = get_db()
            user = get_user(db, message.from_user.id)
            close_db()
            if user.role < role:
                return error_cb(message, user)
            return func(message, *args, **kwargs)
        return wrapper
    return role_required_decor
