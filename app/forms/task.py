from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from datetime import datetime

class TaskForm(FlaskForm):
    title = StringField('Название задачи', validators=[
        DataRequired(),
        Length(min=3, max=100, message='Название должно быть от 3 до 100 символов')
    ])
    description = TextAreaField('Описание', validators=[Optional()])
    due_date = DateTimeField('Срок выполнения', format='%Y-%m-%d %H:%M', 
                            validators=[Optional()],
                            default=datetime.utcnow)
    priority = SelectField('Приоритет', choices=[
        ('Низкий', 'Низкий'),
        ('Средний', 'Средний'),
        ('Высокий', 'Высокий')
    ], default='Средний')
    status = SelectField('Статус', choices=[
        ('Новая', 'Новая'),
        ('В работе', 'В работе'),
        ('Завершена', 'Завершена'),
        ('Отложена', 'Отложена')
    ], default='Новая')
    customer_id = SelectField('Клиент', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить') 