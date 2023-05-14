from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from sqlalchemy.exc import OperationalError, IntegrityError

from flask_blog.forms.user import RegistrationForm, LoginForm
from flask_blog.models import User
from flask_blog.models.database import db

auth_app = Blueprint('auth_app', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth_app.login'


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth_app.login'))


@auth_app.route('/login/', methods=['GET', 'POST'], endpoint='login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index_'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user is None:
            return render_template('auth/login.html',
                                   form=form,
                                   error='пользователь не найден')
        if not user.validate_password(form.password.data):
            return render_template(
                'auth/login.html',
                form=form,
                error='Неверное имя пользователя или пароль'
            )
        login_user(user)
        return redirect(url_for('index.index_'))
    return render_template('auth/login.html', form=form)

    # # =================================================================
    # # print()
    # if request.method == 'GET':
    #     return render_template('auth/login.html')
    #
    # username = request.form.get('username')
    # if not username:
    #     return render_template('auth/login.html', error='username not passed')
    #
    # try:
    #     user = User.query.filter_by(username=username).one_or_none()
    # except OperationalError:
    #     user = None
    #
    # if user is None:
    #     return render_template('auth/login.html',
    #                            error=f'user {username} not found')
    # login_user(user)
    # return redirect(url_for('index.index_'))

    # =================================================================
    # user = User.query.filter_by(username=username).one_or_none()
    # if user is None:
    #     return render_template('auth/login.html',
    #                            error=f'user {username} not found')
    # login_user(user)
    # return redirect(url_for('index.index_'))


@auth_app.route('/logout/', endpoint='logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.index_'))


# http://127.0.0.1:8080/auth/secret/
@auth_app.route('/secret/')
@login_required
def secret_view():
    return 'Super secret data'


__all__ = [
    'login_manager',
    'auth_app',
]


@auth_app.route('/register/', methods=['GET', 'POST'], endpoint='register')
def register():
    # prev_url = None
    # print('auth| register: request.referrer:', request.referrer)
    # auth| register: request.referrer: None
    # auth| register: request.referrer: http://127.0.0.1:8090/
    if current_user.is_authenticated:
        # return redirect('/')
        return redirect(url_for('index.index_'))
    error = None
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append('Это имя уже используется')
            return render_template('auth/register.html',
                                   form=form)
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append('Этот адрес уже используется')
            return render_template('auth/register.html',
                                   form=form)
        user = User(username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    is_staff=False)
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            error = 'ОШИБКА: пользователь не создан'
        else:
            login_user(user)
            return redirect(url_for('index.index_'))
    return render_template('auth/register.html', form=form, error=error)
