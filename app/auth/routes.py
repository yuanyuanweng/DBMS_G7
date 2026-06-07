from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.models.user import User
from app.database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = User.verify_password(email, password)
        if user:
            session['user_id'] = user.id
            session['email'] = user.email
            session['role'] = user.role
            login_type = request.form.get('login_type', 'user')
            if login_type == 'admin' and user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif login_type == 'admin' and user.role != 'admin':
                session.clear()
                flash('This account does not have admin access.', 'error')
                return render_template('auth/login.html', form=None, next=request.args.get('next', ''))
            next_url = request.form.get('next')

            if not next_url or not next_url.startswith('/'):
                db = get_db()
                has_applied = db.execute(
                    'SELECT 1 FROM Application WHERE User_ID = ? LIMIT 1',
                    (user.id,)
                ).fetchone()
                next_url = url_for('main.index') if has_applied else url_for('dogs.list_dogs')

            return redirect(next_url)

        flash('Invalid email or password.', 'error')

    return render_template('auth/login.html', form=None, next=request.args.get('next', ''))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html', form=None)
        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return render_template('auth/register.html', form=None)

        success, _ = User.create(email, password)
        if success:
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        flash('Email already registered.', 'error')

    return render_template('auth/register.html', form=None)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
