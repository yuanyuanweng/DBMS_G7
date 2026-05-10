from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    """
    權限鎖。
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # getattr 防止 current_user 沒有 role 屬性時報錯
        if not current_user.is_authenticated or getattr(current_user, 'role', 0) != 1:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
