from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.models.application import Application
from app.models.dog import Dog
from app.database import get_db

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/apply/<int:dog_id>', methods=['GET', 'POST'])
def apply(dog_id):
    if not session.get('user_id'):
        return redirect(url_for('auth.login') + f'?next={request.url}')

    dog = Dog.get_by_id(dog_id)
    if not dog:
        return redirect(url_for('dogs.list_dogs'))

    user_id = session['user_id']

    if Application.already_applied(user_id, dog_id):
        flash(f'You have already applied for {dog.name}.', 'info')
        return redirect(url_for('applications.my_applications'))

    if request.method == 'POST':
        success, _ = Application.create(user_id, dog_id)
        if success:
            flash(f'Application for {dog.name} submitted successfully!', 'success')
            return redirect(url_for('applications.my_applications'))
        flash('Could not submit application. Please try again.', 'error')

    return render_template('applications/apply.html', dog=dog)

@applications_bp.route('/my-applications')
def my_applications():
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    apps = Application.get_by_user(user_id)
    db = get_db()
    db.execute('UPDATE Application SET Seen = 1 WHERE User_ID = ? AND Seen = 0', (user_id,))
    db.commit()

    return render_template('applications/my_applications.html', applications=apps)

@applications_bp.route('/applications/<int:app_id>/cancel', methods=['POST'])
def cancel(app_id):
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    Application.cancel(app_id, session['user_id'])
    flash('Application withdrawn.', 'info')
    return redirect(url_for('applications.my_applications'))
