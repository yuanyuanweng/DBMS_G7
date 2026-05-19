from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.auth.utils import admin_required
from app.models.dog import Dog, MOCK_DOGS  # 引入寫好的 Dog 和原始資料清單

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    "後台數據動態統計"
    all_dogs_list = Dog.get_all()
    stats = {
        'total_users': 156,
        'total_dogs': len(all_dogs_list), 
        'pending_dogs': len([dog for dog in all_dogs_list if dog.availability == 'Pending']),
        'success_adoptions': len([dog for dog in all_dogs_list if dog.availability == 'Adopted']),
        'admin_name': session.get('username', '管理員')
    }
    
    # 將目前的狗狗清單傳給前端，讓後台表格可以顯示
    return render_template('admin/dashboard.html', stats=stats, dogs=all_dogs_list)


@admin_bp.route('/dog/add', methods=['POST'])
@admin_required
def add_dog():
    "核心新功能：管理員上架新狗狗"
    # 接收後台表單資料
    name = request.form.get('name')
    breed = request.form.get('breed')
    age = request.form.get('age')
    gender = request.form.get('gender')
    city = request.form.get('city')
    size = request.form.get('size')

    if not name or not breed:
        flash("狗狗名字與品種為必填項目！", "danger")
        return redirect(url_for('admin.dashboard'))

    # 產生新的 Dog_ID
    new_id = max([dog['Dog_ID'] for dog in MOCK_DOGS]) + 1 if MOCK_DOGS else 1

    # 模擬寫入資料庫（直接 append 到MOCK_DOGS 裡）
    new_dog_raw = {
        'Dog_ID': new_id,
        'Shelter_ID': 1,
        'Name': name,
        'Breed': breed,
        'Age': int(age) if age else 0,
        'Gender': gender or 'Male',
        'City': city or 'Taipei',
        'Size': size or 'Medium',
        'Image_URL': None,
        'Availability': 'Available',
        'Is_Urgent': 0,
        'Is_Liked': 0,
        'AI_Story': 'No story yet.',
        'Tags': [f'🏷 {size}', f'{gender}']
    }
    MOCK_DOGS.append(new_dog_raw)
    
    flash(f"成功上架新狗狗：{name}！", "success")
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/dog/delete/<int:dog_id>', methods=['POST'])
@admin_required
def delete_dog(dog_id):
    "核心新功能：管理員下架/刪除狗狗"
    global MOCK_DOGS
    
    # 尋找並移除該 ID 的狗狗
    for i, dog in enumerate(MOCK_DOGS):
        if dog['Dog_ID'] == dog_id:
            removed_dog = MOCK_DOGS.pop(i)
            flash(f"已成功下架狗狗：{removed_dog['Name']}", "warning")
            return redirect(url_for('admin.dashboard'))
            
    flash("找不到該狗狗資料", "danger")
    return redirect(url_for('admin.dashboard'))