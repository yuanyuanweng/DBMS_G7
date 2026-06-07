from functools import wraps
from flask import session, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash("Please log in first.", "error")
            return redirect(url_for('auth.login', next=request.full_path))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 檢查 session 中是否有 user_id 且角色是否為 admin
        if not session.get('user_id') or session.get('role') != 'admin':
            flash("Permission denied. Administrator access only.", "error")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    "將明文密碼加密"
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    "驗證密碼是否正確"
    return check_password_hash(hashed_password, password)
