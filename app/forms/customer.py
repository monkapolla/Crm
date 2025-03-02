from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class CustomerForm(FlaskForm):
    name = StringField('Название/Имя клиента', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Название должно быть от 2 до 100 символов')
    ])
    company = StringField('Компания', validators=[Optional(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(message='Введите корректный email адрес')])
    phone = StringField('Телефон', validators=[Optional(), Length(max=20)])
    address = StringField('Адрес', validators=[Optional(), Length(max=200)])
    status = SelectField('Статус', choices=[
        ('Новый', 'Новый'),
        ('Активный', 'Активный'),
        ('Неактивный', 'Неактивный')
    ])
    notes = TextAreaField('Примечания', validators=[Optional()])
    submit = SubmitField('Сохранить')

class ContactForm(FlaskForm):
    first_name = StringField('Имя', validators=[
        DataRequired(),
        Length(min=2, max=50, message='Имя должно быть от 2 до 50 символов')
    ])
    last_name = StringField('Фамилия', validators=[
        DataRequired(),
        Length(min=2, max=50, message='Фамилия должна быть от 2 до 50 символов')
    ])
    position = StringField('Должность', validators=[Optional(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(message='Введите корректный email адрес')])
    phone = StringField('Телефон', validators=[Optional(), Length(max=20)])
    is_primary = BooleanField('Основной контакт')
    notes = TextAreaField('Примечания', validators=[Optional()])
    submit = SubmitField('Сохранить') 