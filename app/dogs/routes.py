from flask import Blueprint, render_template, request, current_app, session, jsonify
import sqlite3

dogs_bp = Blueprint('dogs', __name__, url_prefix='/dogs')

PER_PAGE = 12


def get_db():
    conn = sqlite3.connect(current_app.config['DB_PATH'])
    conn.row_factory = lambda c, r: {col[0]: r[i] for i, col in enumerate(c.description)}
    return conn


class Pagination:
    def __init__(self, page, pages):
        self.page = page
        self.pages = pages
        self.has_prev = page > 1
        self.has_next = page < pages
        self.prev_num = page - 1
        self.next_num = page + 1


@dogs_bp.route('/')
def list():
    from app.models.dog import Dog

    q    = request.args.get('q', '').strip()
    page = max(1, int(request.args.get('page', 1) or 1))

    db = get_db()
    where, params = [], []
    if q:
        where.append("(Name LIKE ? OR Breed LIKE ?)")
        params += [f'%{q}%', f'%{q}%']
    clause = ('WHERE ' + ' AND '.join(where)) if where else ''

    total = db.execute(f"SELECT COUNT(*) as c FROM Dog {clause}", params).fetchone()['c']
    pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    page  = min(page, pages)
    rows  = db.execute(
        f"SELECT * FROM Dog {clause} ORDER BY Dog_ID LIMIT ? OFFSET ?",
        params + [PER_PAGE, (page - 1) * PER_PAGE]
    ).fetchall()
    db.close()

    dogs      = [Dog(r) for r in rows]
    liked_ids = set(session.get('liked_ids', []))
    stats     = {'available': total, 'adopted': 342}

    return render_template(
        'dogs/list.html',
        dogs=dogs,
        dogs_json=[d.to_dict() for d in dogs],
        pagination=Pagination(page, pages),
        stats=stats,
        liked_ids=liked_ids,
    )


@dogs_bp.route('/<int:id>')
def detail(id):
    from app.models.dog import Dog

    db  = get_db()
    row = db.execute("SELECT * FROM Dog WHERE Dog_ID = ?", [id]).fetchone()
    db.close()

    if row is None:
        return "Dog not found", 404

    return render_template('dogs/detail.html', dog=Dog(row), already_applied=False)


@dogs_bp.route('/<int:id>/like', methods=['POST'])
def like(id):
    liked = set(session.get('liked_ids', []))
    if id in liked:
        liked.discard(id)
    else:
        liked.add(id)
    session['liked_ids'] = list(liked)
    return jsonify({'status': 'ok', 'liked': id in liked})
