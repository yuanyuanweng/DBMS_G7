from flask import Blueprint, render_template, session
from app.auth.utils import admin_required
# 之後要對接資料庫模型
# from app.models import User, Dog, db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    "後台儀表板主頁"
    
    # 開發構想：統計數據 (暫時使用 Mock Data) ---
    # 未來會改為 User.query.count() 等資料庫查詢
    stats = {
        'total_users': 156,        # 總註冊人數
        'pending_dogs': 12,        # 待審核/待領養狗狗
        'success_adoptions': 45,   # 成功領養案例
        'admin_name': session.get('username', '管理員')
    }
    
    # 模擬最近的活動紀錄
    recent_activities = [
        {'time': '10分鐘前', 'event': '新用戶註冊: Sophia'},
        {'time': '1小時前', 'event': '狗狗資料更新: Kosomo'},
        {'time': '2小時前', 'event': '系統權限變更'}
    ]

    return render_template(
        'admin/dashboard.html', 
        stats=stats, 
        activities=recent_activities
    )