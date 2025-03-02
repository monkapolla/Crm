from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Task, Customer
from app.forms.task import TaskForm
from datetime import datetime

task_bp = Blueprint('task', __name__, url_prefix='/tasks')

@task_bp.route('/')
@login_required
def index():
    status_filter = request.args.get('status', '')
    if status_filter:
        tasks = Task.query.filter_by(
            user_id=current_user.id,
            status=status_filter
        ).order_by(Task.due_date.asc()).all()
    else:
        tasks = Task.query.filter_by(
            user_id=current_user.id
        ).order_by(Task.due_date.asc()).all()
    
    return render_template('task/index.html',
                          title='Мои задачи',
                          tasks=tasks,
                          status_filter=status_filter)

@task_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TaskForm()
    # Заполняем поле выбора клиента
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.order_by(Customer.name).all()]
    
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            status=form.status.data,
            customer_id=form.customer_id.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Задача добавлена!', 'success')
        return redirect(url_for('task.index'))
    
    return render_template('task/form.html',
                          title='Добавить задачу',
                          form=form)

@task_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    task = Task.query.get_or_404(id)
    # Проверяем, принадлежит ли задача текущему пользователю
    if task.user_id != current_user.id:
        flash('У вас нет доступа к этой задаче', 'danger')
        return redirect(url_for('task.index'))
    
    form = TaskForm(obj=task)
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.order_by(Customer.name).all()]
    
    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        flash('Задача обновлена!', 'success')
        return redirect(url_for('task.view', id=task.id))
    
    return render_template('task/form.html',
                          title='Редактировать задачу',
                          form=form)

@task_bp.route('/<int:id>')
@login_required
def view(id):
    task = Task.query.get_or_404(id)
    # Проверяем, принадлежит ли задача текущему пользователю
    if task.user_id != current_user.id:
        flash('У вас нет доступа к этой задаче', 'danger')
        return redirect(url_for('task.index'))
    
    return render_template('task/view.html',
                          title=task.title,
                          task=task)

@task_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    # Проверяем, принадлежит ли задача текущему пользователю
    if task.user_id != current_user.id:
        flash('У вас нет доступа к этой задаче', 'danger')
        return redirect(url_for('task.index'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Задача удалена!', 'success')
    return redirect(url_for('task.index'))

@task_bp.route('/<int:id>/complete', methods=['POST'])
@login_required
def complete(id):
    task = Task.query.get_or_404(id)
    # Проверяем, принадлежит ли задача текущему пользователю
    if task.user_id != current_user.id:
        flash('У вас нет доступа к этой задаче', 'danger')
        return redirect(url_for('task.index'))
    
    task.status = 'Завершена'
    task.completed_at = datetime.utcnow()
    db.session.commit()
    flash('Задача отмечена как завершенная!', 'success')
    return redirect(url_for('task.index')) 