from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from .utils import hash_password, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 接收前端登入資料
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')

        # 智慧角色分流
        # 模擬兩組帳號先測試不同的跳轉結果
        users_db = {
            "admin": {"password": "123", "role": "admin"},
            "user": {"password": "123", "role": "user"}
        }

        if username in users_db and password == users_db[username]['password']:
            # 登入成功將身份寫入 Session
            session['user_id'] = 101
            session['username'] = username
            session['role'] = users_db[username]['role']

            flash(f"登入成功！歡迎 {username}", "success")

            # 智慧跳轉
            if session['role'] == 'admin':
                # 跳轉至寫好的 Dashboard
                return redirect(url_for('admin.dashboard'))
            else:
                # 配合會議結論：一般使用者跳轉至「我的申請」頁面
                return redirect(url_for('applications.my_applications'))

        flash("帳號或密碼錯誤", "danger")
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    "徹底清理 Session"
    session.clear()
    flash("您已成功登出", "info")
    return redirect(url_for('auth.login'))