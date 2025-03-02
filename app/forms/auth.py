from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User, Role

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=3, max=64, message='Имя пользователя должно быть от 3 до 64 символов')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Введите корректный email адрес')
    ])
    first_name = StringField('Имя', validators=[Optional(), Length(max=30)])
    last_name = StringField('Фамилия', validators=[Optional(), Length(max=30)])
    position = StringField('Должность', validators=[Optional(), Length(max=50)])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, message='Пароль должен содержать минимум 8 символов')
    ])
    password2 = PasswordField('Повторите пароль', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот email уже зарегистрирован. Пожалуйста, используйте другой.')

class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=3, max=64, message='Имя пользователя должно быть от 3 до 64 символов')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Введите корректный email адрес')
    ])
    first_name = StringField('Имя', validators=[Optional(), Length(max=30)])
    last_name = StringField('Фамилия', validators=[Optional(), Length(max=30)])
    position = StringField('Должность', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Сохранить изменения')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Этот email уже зарегистрирован. Пожалуйста, используйте другой.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[
        DataRequired(),
        Length(min=8, message='Пароль должен содержать минимум 8 символов')
    ])
    confirm_password = PasswordField('Подтвердите новый пароль', validators=[
        DataRequired(),
        EqualTo('new_password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Изменить пароль')

class UserManagementForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    first_name = StringField('Имя', validators=[Optional(), Length(max=30)])
    last_name = StringField('Фамилия', validators=[Optional(), Length(max=30)])
    position = StringField('Должность', validators=[Optional(), Length(max=50)])
    role = SelectField('Роль', choices=Role.get_choices(), validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[
        Optional(),
        Length(min=8, message='Пароль должен содержать минимум 8 символов')
    ])
    password2 = PasswordField('Повторите пароль', validators=[
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Сохранить') 