from flask import Blueprint, render_template, session
from app.auth.utils import admin_required
# 1. 成功引進璋珣寫好的 Dog 類別
from app.models.dog import Dog  

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    "後台儀表板主頁：串接真實 Dog 物件資料"
    
    # 2.取得目前系統中所有的狗狗物件列表
    all_dogs_list = Dog.get_all()
    
    # 利用實體資料動態統計 
    # 這裡的統計數據會隨 models/dog.py 裡的 MOCK_DOGS 內容自動更新
    stats = {
        'total_users': 156, # 這一行之後等璋珣把 user.py 寫好，我們再改成 User.query.count()
        
        # 動態計算：算算看清單裡有幾隻狗狗
        'total_dogs': len(all_dogs_list), 
        
        # 動態計算：算算看狀態是 'Pending'（審核中）的狗狗有幾隻
        'pending_dogs': len([dog for dog in all_dogs_list if dog.availability == 'Pending']),
        
        # 動態計算：算算看狀態是 'Adopted'（已領養）的狗狗有幾隻
        'success_adoptions': len([dog for dog in all_dogs_list if dog.availability == 'Adopted']),
        
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