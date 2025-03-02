from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Role:
    ADMIN = 'admin'  # Полный доступ ко всему
    MANAGER = 'manager'  # Управление клиентами и задачами, создание отчетов
    EMPLOYEE = 'employee'  # Базовый доступ (работа с клиентами и задачами) 
    VIEWER = 'viewer'  # Только просмотр (без редактирования)
    
    @classmethod
    def get_choices(cls):
        return [
            (cls.ADMIN, 'Администратор'),
            (cls.MANAGER, 'Менеджер'),
            (cls.EMPLOYEE, 'Сотрудник'),
            (cls.VIEWER, 'Наблюдатель')
        ]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=Role.EMPLOYEE)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    position = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Отношения
    tasks = db.relationship('Task', backref='assigned_to', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == Role.ADMIN
    
    def is_manager(self):
        return self.role == Role.MANAGER or self.role == Role.ADMIN
    
    def is_employee(self):
        return self.role == Role.EMPLOYEE or self.is_manager()
    
    def is_viewer(self):
        return self.role == Role.VIEWER
    
    def can_create(self):
        return self.role in [Role.ADMIN, Role.MANAGER, Role.EMPLOYEE]
    
    def can_edit(self):
        return self.role in [Role.ADMIN, Role.MANAGER, Role.EMPLOYEE]
    
    def can_delete(self):
        return self.role in [Role.ADMIN, Role.MANAGER]
    
    def can_manage_users(self):
        return self.role == Role.ADMIN
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def get_role_display(self):
        for role_value, role_name in Role.get_choices():
            if self.role == role_value:
                return role_name
        return 'Неизвестно'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Новый')  # Новый, Активный, Неактивный
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношения
    contacts = db.relationship('Contact', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    is_primary = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Внешние ключи
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    
    def __repr__(self):
        return f'<Contact {self.first_name} {self.last_name}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.String(20), default='Средний')  # Низкий, Средний, Высокий
    status = db.Column(db.String(20), default='Новая')  # Новая, В работе, Завершена, Отложена
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Внешние ключи
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Task {self.title}>' 