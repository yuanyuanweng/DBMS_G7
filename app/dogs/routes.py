from flask import Blueprint, render_template, request

dogs_bp = Blueprint('dogs', __name__)

@dogs_bp.route('/')
@dogs_bp.route('/dogs')
def list():
    # 接收搜尋參數
    query = request.args.get('q', '')
    city = request.args.get('city', '')
    
    # 核心模擬資料 (欄位對應 list.html)
    all_dogs = [
        {
            'id': 1,
            'name': 'Komame',
            'breed': 'Shiba Inu Mix',
            'age': '2 yrs',
            'gender': 'Female',
            'city': 'Taipei',
            'is_urgent': True,
            'tags': ['Apartment-Friendly', 'Gentle'],
            'image_url': None, # 讓 HTML 跑預設 SVG
            'ai_story': 'I love napping in sunny spots.',
            'color': '#D9A57A',
            'spot_color': '#C4714A'
        }
    ]

    # 基礎搜尋邏輯
    filtered_dogs = [
        d for d in all_dogs 
        if query.lower() in d['name'].lower() or query.lower() in d['breed'].lower()
    ] if query else all_dogs

    return render_template(
        'list.html', 
        dogs=filtered_dogs, 
        stats={'available': 128, 'adopted': 342}, # Hero 區塊數據
        liked_ids=[],
        dogs_json=filtered_dogs # 供前端 JS 使用
    )

@dogs_bp.route('/dog/<int:id>')
def detail(id):
    return render_template('detail.html', dog_id=id)
