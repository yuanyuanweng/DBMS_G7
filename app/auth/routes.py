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

@auth_bp.route('/favorite/<int:dog_id>', methods=['POST'])
def toggle_favorite(dog_id):
    '''
   新增/取消收藏狗狗功能 (純後端 API)
    '''
    # 安全檢查：確認用戶有沒有登入
    if 'username' not in session:
        return jsonify({
            'success': False, 
            'message': '請先登入後再進行收藏！'
        }), 401

    # 引入剛才修改好的 MOCK_DOGS 假資料來模擬資料庫操作
    from app.models.dog import MOCK_DOGS
    
    # 尋找有沒有這隻狗
    target_dog = None
    for dog in MOCK_DOGS:
        if dog['Dog_ID'] == dog_id:
            target_dog = dog
            break
            
    if not target_dog:
        return jsonify({
            'success': False, 
            'message': '找不到該隻狗狗的資料'
        }), 404

    # 如果是 0 就變 1（收藏），如果是 1 就變 0（取消收藏）
    if target_dog.get('Is_Liked', 0) == 0:
        target_dog['Is_Liked'] = 1
        status_msg = f"成功將 {target_dog['Name']} 加入收藏清單！"
        action = "added"
    else:
        target_dog['Is_Liked'] = 0
        status_msg = f"已將 {target_dog['Name']} 從收藏清單移除"
        action = "removed"

    # 回傳標準 JSON 規格給前端
    return jsonify({
        'success': True,
        'message': status_msg,
        'action': action,
        'dog_id': dog_id
    }), 200

@auth_bp.app_template_global('dog_list')
def rescue_dog_list(dog_id):
    return url_for('dogs.list_dogs', dog_id=dog_id)


@auth_bp.app_template_global('rescue_dogs_list_url')
def rescue_dogs_list_url():
    return url_for('dogs.list_dogs')

@auth_bp.app_template_global('rescue_dogs_edit_url')
def rescue_dogs_edit_url(dog_id):
    return url_for('dogs.edit', dog_id=dog_id)