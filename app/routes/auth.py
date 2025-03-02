from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from datetime import datetime
from app import db
from app.models import User, Role
from app.forms.auth import LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm, UserManagementForm
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('У вас нет доступа к этой странице.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_manager():
            flash('У вас нет доступа к этой странице.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        # Обновляем время последнего входа
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        flash('Вы успешно вошли в систему!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Вход', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            position=form.position.data,
            role=Role.EMPLOYEE  # По умолчанию регистрация даёт роль сотрудника
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы! Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Регистрация', form=form)

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(original_username=current_user.username, original_email=current_user.email)
    password_form = ChangePasswordForm()
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.position = form.position.data
        db.session.commit()
        flash('Ваш профиль успешно обновлен!', 'success')
        return redirect(url_for('auth.profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.position.data = current_user.position
    
    return render_template('auth/profile.html', title='Мой профиль', 
                          form=form, password_form=password_form)

@auth_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Неверный текущий пароль', 'danger')
            return redirect(url_for('auth.profile'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Ваш пароль успешно изменен!', 'success')
        return redirect(url_for('auth.profile'))
    
    flash('Произошла ошибка при изменении пароля. Проверьте введенные данные.', 'danger')
    return redirect(url_for('auth.profile'))

@auth_bp.route('/users')
@login_required
@admin_required
def users_list():
    users = User.query.all()
    return render_template('auth/users_list.html', title='Управление пользователями', users=users)

@auth_bp.route('/users/new', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = UserManagementForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Это имя пользователя уже занято.', 'danger')
            return render_template('auth/user_form.html', title='Добавление пользователя', form=form)
            
        if User.query.filter_by(email=form.email.data).first():
            flash('Этот email уже зарегистрирован.', 'danger')
            return render_template('auth/user_form.html', title='Добавление пользователя', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            position=form.position.data,
            role=form.role.data
        )
        
        if form.password.data:
            user.set_password(form.password.data)
        else:
            # Устанавливаем стандартный пароль, который нужно будет изменить
            user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        flash(f'Пользователь {user.username} успешно создан!', 'success')
        return redirect(url_for('auth.users_list'))
    
    return render_template('auth/user_form.html', title='Добавление пользователя', form=form)

@auth_bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserManagementForm(obj=user)
    
    if form.validate_on_submit():
        username_exists = User.query.filter(User.username == form.username.data, User.id != id).first()
        if username_exists:
            flash('Это имя пользователя уже занято.', 'danger')
            return render_template('auth/user_form.html', title='Редактирование пользователя', form=form, user=user)
            
        email_exists = User.query.filter(User.email == form.email.data, User.id != id).first()
        if email_exists:
            flash('Этот email уже зарегистрирован.', 'danger')
            return render_template('auth/user_form.html', title='Редактирование пользователя', form=form, user=user)
        
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.position = form.position.data
        user.role = form.role.data
        
        if form.password.data:
            user.set_password(form.password.data)
        
        db.session.commit()
        flash(f'Данные пользователя {user.username} успешно обновлены!', 'success')
        return redirect(url_for('auth.users_list'))
    
    return render_template('auth/user_form.html', title='Редактирование пользователя', form=form, user=user)

@auth_bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    
    if user == current_user:
        flash('Вы не можете удалить свою учетную запись.', 'danger')
        return redirect(url_for('auth.users_list'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'Пользователь {username} успешно удален.', 'success')
    return redirect(url_for('auth.users_list')) 