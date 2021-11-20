from functools import wraps

from models import get_user, db_required


def user_required(func):
    @wraps(func)
    @db_required
    def wrapper(message, db, *args, **kwargs):
        user = get_user(db, message.from_user.id)
        return func(message, *args, **kwargs, user=user)
    return wrapper


def role_required(role, error_cb):
    def role_required_decor(func):
        @user_required
        @wraps(func)
        def wrapper(message, user, *args, **kwargs):
            if user.role < role:
                return error_cb(message, user)
            return func(message, *args, **kwargs, user=user)
        return wrapper
    return role_required_decor
