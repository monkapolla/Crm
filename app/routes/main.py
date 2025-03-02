from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Customer, Task
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html', title='Главная страница')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Получаем статистику для дашборда
    total_customers = Customer.query.count()
    active_customers = Customer.query.filter_by(status='Активный').count()
    potential_customers = Customer.query.filter_by(status='Потенциальный').count()
    inactive_customers = Customer.query.filter_by(status='Неактивный').count()
    
    # Последние добавленные клиенты
    recent_customers = Customer.query.order_by(Customer.created_at.desc()).limit(5).all()
    
    # Задачи пользователя
    user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).all()
    
    # Просроченные задачи
    overdue_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.status != 'Завершена',
        Task.due_date < datetime.utcnow()
    ).count()
    
    # Задачи на сегодня
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)
    today_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.status != 'Завершена',
        Task.due_date >= today,
        Task.due_date < tomorrow
    ).count()
    
    # Статистика по задачам по статусам
    total_tasks = Task.query.filter_by(user_id=current_user.id).count()
    new_tasks = Task.query.filter_by(user_id=current_user.id, status='Новая').count()
    in_progress_tasks = Task.query.filter_by(user_id=current_user.id, status='В работе').count()
    completed_tasks = Task.query.filter_by(user_id=current_user.id, status='Завершена').count()
    postponed_tasks = Task.query.filter_by(user_id=current_user.id, status='Отложена').count()
    
    # Текущая дата для отображения на дашборде
    now = datetime.utcnow()
    
    return render_template('main/dashboard.html', 
                          title='Панель управления',
                          total_customers=total_customers,
                          active_customers=active_customers,
                          potential_customers=potential_customers,
                          inactive_customers=inactive_customers,
                          recent_customers=recent_customers,
                          user_tasks=user_tasks,
                          overdue_tasks=overdue_tasks,
                          today_tasks=today_tasks,
                          now=now,
                          total_tasks=total_tasks,
                          new_tasks=new_tasks,
                          in_progress_tasks=in_progress_tasks,
                          completed_tasks=completed_tasks,
                          postponed_tasks=postponed_tasks)

@main_bp.route('/about')
def about():
    return render_template('main/about.html', title='О системе') 