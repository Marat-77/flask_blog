from flask import Blueprint, render_template
from flask_login import LoginManager
from sqlalchemy.exc import OperationalError
from werkzeug.exceptions import NotFound

from flask_blog.models import User
from flask_blog.users.mock_users import USERS
from flask_blog.articles.mock_articles import ARTICLES

user = Blueprint('user',
                 __name__,
                 url_prefix='/users',
                 # static_folder='../static'
                 )


@user.route('/')
def users_list():
    try:
        users = User.query.all()
        return render_template('users/users_list.html',
                               # users=USERS,
                               users=users,
                               )
    except OperationalError:
        raise NotFound
    # users = User.query.all()
    # return render_template('users/users_list.html',
    #                        # users=USERS,
    #                        users=users,
    #                        )


@user.route('/<int:pk>/')
def user_detail(pk: int):
    try:
        user_ = User.query.filter_by(id=pk).one_or_none()
        if user_ is None:
            raise NotFound(f'Пользователь #{pk} не найден')
        full_name = f'{user_.username}.'
        if user_.last_name:
            full_name += f'{user_.last_name}'
        if user_.first_name:
            full_name += f'{user_.first_name}'
        articles_id = user_articles(pk)
        return render_template('users/user_detail.html',
                               full_name=full_name,
                               articles_id=articles_id,
                               articles=ARTICLES)
    except OperationalError:
        raise NotFound
    # user_ = User.query.filter_by(id=pk).one_or_none()
    # # print(user)
    # # print(user.last_name)
    # # print(user.first_name)
    # if user_ is None:
    #     raise NotFound(f'Пользователь #{pk} не найден')
    # # return render_template()
    # full_name = f'{user_.username}.'
    # if user_.last_name:
    #     full_name += f'{user_.last_name}'
    # if user_.first_name:
    #     full_name += f'{user_.first_name}'
    # # print(full_name)
    # articles_id = user_articles(pk)
    # return render_template('users/user_detail.html',
    #                        full_name=full_name,
    #                        articles_id=articles_id,
    #                        articles=ARTICLES)
    # if pk in USERS:
    #     full_name = f'{USERS[pk].get("last_name")} {USERS[pk].get("first_name")}'
    #     articles_id = user_articles(pk)
    #     return render_template('users/user_detail.html',
    #                            full_name=full_name,
    #                            articles_id=articles_id,
    #                            articles=ARTICLES)
    # raise NotFound


def user_articles(pk: int):
    author_art = []
    for i in ARTICLES:
        if ARTICLES[i].get('article_author') == pk:
            author_art.append(i)
    return author_art
