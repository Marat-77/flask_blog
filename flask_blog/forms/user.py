from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo


class UserForm(FlaskForm):
    username = StringField('username', [DataRequired(),
                                        Length(max=155)])
    first_name = StringField('Имя', [Optional(), Length(max=155)])
    last_name = StringField('Фамилия', [Length(max=155)])
    email = StringField('email',
                        [DataRequired(),
                         Email(),
                         Length(min=4, max=255)],
                        filters=[lambda data: data and data.lower()])


class RegistrationForm(UserForm):
    password = PasswordField(
        'Пароль',
        [DataRequired(),
         EqualTo('password_confirm',
                 message='Пароль должен совпадать с подтверждением')]
    )
    password_confirm = PasswordField('Подтверждение пароля')
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('username', [DataRequired(),
                                        Length(max=155)])
    password = PasswordField(
        'Пароль',
        [DataRequired()]
    )
    submit = SubmitField('Войти')
