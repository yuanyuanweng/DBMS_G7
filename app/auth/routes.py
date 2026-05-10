from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from .utils import hash_password, verify_password
# from app.models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 支援前端 JSON 或是 Form 表單
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "請輸入帳號密碼"}), 400

        # 加密密碼
        hashed_pw = hash_password(password)

        #資料庫邏輯 (模擬) 
        # new_user = User(username=username, password=hashed_pw, role='user')
        # db.session.add(new_user)
        # db.session.commit()
        # ----------------------------

        return jsonify({
            "message": "註冊成功！",
            "user": username,
            "debug_hashed_password": hashed_pw
        }), 201

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 登入邏輯可以在此擴充
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("你已成功登出", "info")
    return redirect(url_for('auth.login'))