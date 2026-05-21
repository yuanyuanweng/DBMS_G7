from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from app.auth.utils import admin_required
from app.database import get_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    db = get_db()

    total_users = db.execute('SELECT COUNT(*) FROM Users').fetchone()[0]
    pending_count = db.execute("SELECT COUNT(*) FROM Application WHERE Status = 0").fetchone()[0]
    approved_count = db.execute("SELECT COUNT(*) FROM Application WHERE Status = 1").fetchone()[0]
    rejected_count = db.execute("SELECT COUNT(*) FROM Application WHERE Status = 2").fetchone()[0]

    applications = db.execute('''
        SELECT a.App_ID, a.Status, a.Created_at,
               u.Email, u.User_ID,
               d.Name AS Dog_Name, d.Dog_ID
        FROM Application a
        JOIN Users u ON a.User_ID = u.User_ID
        JOIN Dog d ON a.Dog_ID = d.Dog_ID
        ORDER BY a.Created_at DESC
        LIMIT 20
    ''').fetchall()

    users = db.execute(
        'SELECT User_ID, Email, Role FROM Users ORDER BY User_ID DESC'
    ).fetchall()

    STATUS_MAP = {0: 'Pending', 1: 'Approved', 2: 'Rejected'}

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        pending_count=pending_count,
        approved_count=approved_count,
        rejected_count=rejected_count,
        applications=applications,
        users=users,
        STATUS_MAP=STATUS_MAP,
        admin_email=session.get('email', '')
    )

@admin_bp.route('/applications/<int:app_id>/status', methods=['POST'])
@admin_required
def update_status(app_id):
    new_status = request.form.get('status')
    if new_status not in ('0', '1', '2'):
        flash('Invalid status.', 'error')
        return redirect(url_for('admin.dashboard'))

    db = get_db()
    db.execute('UPDATE Application SET Status = ? WHERE App_ID = ?', (int(new_status), app_id))
    db.commit()
    flash('Application status updated.', 'success')
    return redirect(url_for('admin.dashboard'))