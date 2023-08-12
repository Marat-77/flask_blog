import flask_login
# import requests
from flask import Blueprint, redirect, url_for, request, render_template, \
    session
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from requests import JSONDecodeError
# from sqlalchemy.exc import OperationalError, IntegrityError
from werkzeug.exceptions import NotFound

from flask_front.forms.user import RegistrationForm, LoginForm
# from flask_front.models import User
# from flask_front.models.database import db
from flask_front.request_api.api_request import get_from_api, post_to_api

auth_app = Blueprint('auth_app', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth_app.login'


class UserLogin(flask_login.UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id: int):
    api_path = f'/api/users/{user_id}'
    get_user_ = get_from_api(api_path)
    user = None
    if get_user_.ok:
        get_user_ = get_user_.json()
        user = UserLogin()
        user.id = get_user_.get('user_id')
        user.username = get_user_.get('username')
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth_app.login'))


@auth_app.route('/login/', methods=['GET', 'POST'], endpoint='login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index_'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        payload = {'username': form.username.data,
                   'password': form.password.data}
        api_path_login = f'/api/login/'
        api_login = post_to_api(api_path_login, to_api_payload=payload)
        if api_login.status_code == 401:
            print('r.request:', api_login.request)
            error_json = api_login.json()
            return render_template(
                'auth/login.html',
                form=form,
                error=error_json.get('error')
            )

        try:
            get_token = api_login.json()
        except Exception as err:
            print('login error:', err)
            raise NotFound
        else:
            access_token = get_token.get('access_token')
            refresh_token = get_token.get('refresh_token')
            api_user = get_token.get('user')
            if refresh_token is not None:
                session['_refresh_token'] = refresh_token
            user = UserLogin()
            user.id = api_user.get('user_id')
            user.username = api_user.get('username')
            login_user(user)
            if session.get('next_url') is not None:
                x_next = session.pop('next_url')
                return redirect(x_next)
            return redirect(url_for('index.index_'))
    session['next_url'] = request.referrer
    return render_template('auth/login.html', form=form)


@auth_app.route('/logout/', endpoint='logout')
@login_required
def logout():
    if "_access_token" in session:
        session.pop("_access_token")
        session.pop("_refresh_token")
    logout_user()
    return redirect(url_for('index.index_'))


__all__ = [
    'login_manager',
    'auth_app',
]


@auth_app.route('/register/', methods=['GET', 'POST'], endpoint='register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.user_detail', pk=current_user.id))
    error = None
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        payload = {'username': form.username.data,
                   'password': form.password.data,
                   'first_name': form.first_name.data,
                   'last_name': form.last_name.data,
                   'email': form.email.data}
        api_path_register = f'/api/register/'
        api_register = post_to_api(api_path_register,
                                   to_api_payload=payload)

        if not api_register.ok:
            error = 'ОШИБКА: пользователь не создан'
            return render_template('auth/register.html',
                                   form=form,
                                   error=error)
        user = UserLogin()
        try:
            api_user = api_register.json()
            user.id = api_user.get('id')
            user.username = api_user.get('username')
        except JSONDecodeError:
            raise NotFound
        else:
            login_user(user)
            return redirect(url_for('user.user_detail', pk=user.id))
    return render_template('auth/register.html', form=form, error=error)
