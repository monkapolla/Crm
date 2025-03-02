import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Инициализируем расширения
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(test_config=None):
    # Создаем и настраиваем приложение
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'crm.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # Загружаем конфигурацию экземпляра, если она существует
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Загружаем тестовую конфигурацию
        app.config.from_mapping(test_config)

    # Убеждаемся, что директория instance существует
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Инициализируем расширения с приложением
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Регистрируем модели
    from app.models import User, Customer, Contact, Task
    
    # Регистрируем blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.customer import customer_bp
    from app.routes.task import task_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(task_bp)
    
    # Добавляем команду для инициализации базы данных
    @app.cli.command('init-db')
    def init_db_command():
        """Очищает существующие данные и создает новые таблицы."""
        db.drop_all()
        db.create_all()
        print('Инициализирована база данных.')
        
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    return app 