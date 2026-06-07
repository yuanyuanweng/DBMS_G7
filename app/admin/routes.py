from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from app.auth.utils import admin_required
from app.models.application import Application, STATUS_MAP

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    counts = Application.get_admin_counts()

    return render_template(
        'admin/dashboard.html',
        total_users=Application.count_users(),
        pending_count=counts["pending_count"],
        approved_count=counts["approved_count"],
        rejected_count=counts["rejected_count"],
        applications=Application.get_recent_for_admin(limit=20),
        users=Application.get_admin_users(),
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

    success, message = Application.update_status(app_id, int(new_status))
    if not success:
        flash(message, 'error')
        return redirect(url_for('admin.dashboard'))

    flash('Application status updated.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/applications/<int:app_id>/delete', methods=['POST'])
@admin_required
def delete_application(app_id):
    if not Application.delete_by_id(app_id):
        flash('Application not found.', 'error')
        return redirect(url_for('admin.dashboard'))

    flash('Application deleted.', 'success')
    return redirect(url_for('admin.dashboard'))
