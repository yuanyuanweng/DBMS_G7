from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.auth.utils import login_required
from app.models.application import Application
from app.models.dog import Dog

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/apply/<int:dog_id>', methods=['GET', 'POST'])
@login_required
def apply(dog_id):
    dog = Dog.get_by_id(dog_id)
    if not dog:
        return redirect(url_for('dogs.list_dogs'))

    user_id = session['user_id']

    if Application.already_applied(user_id, dog_id):
        flash(f'You have already applied for {dog.name}.', 'info')
        return redirect(url_for('applications.my_applications'))

    if request.method == 'POST':
        form_data = {
            'full_name': request.form.get('full_name', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'city': request.form.get('city', '').strip(),
            'housing_type': request.form.get('house_type', '').strip(),
            'reason': request.form.get('reason', '').strip(),
            'lifestyle': request.form.get('lifestyle', '').strip(),
        }

        success, _ = Application.create(user_id, dog_id, **form_data)
        if success:
            flash(f'Application for {dog.name} submitted successfully!', 'success')
            return redirect(url_for('applications.my_applications'))
        flash('Could not submit application. Please try again.', 'error')

    return render_template('applications/apply.html', dog=dog)

@applications_bp.route('/my-applications')
@login_required
def my_applications():
    user_id = session['user_id']
    Application.mark_updates_seen(user_id)
    apps = Application.get_by_user(user_id)
    return render_template('applications/my_applications.html', applications=apps)

@applications_bp.route('/applications/<int:app_id>/cancel', methods=['POST'])
@login_required
def cancel(app_id):
    Application.cancel(app_id, session['user_id'])
    flash('Application withdrawn.', 'info')
    return redirect(url_for('applications.my_applications'))
