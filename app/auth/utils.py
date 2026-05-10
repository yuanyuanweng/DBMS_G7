from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 檢查 session 中是否有 user_id 且角色是否為 admin
        if not session.get('user_id') or session.get('role') != 'admin':
            flash("權限不足，僅限管理員訪問。", "danger")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    "將明文密碼加密"
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    "驗證密碼是否正確"
    return check_password_hash(hashed_password, password)