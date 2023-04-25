from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from flask_blog.users.mock_users import USERS
from flask_blog.articles.mock_articles import ARTICLES

user = Blueprint('user',
                 __name__,
                 url_prefix='/users',
                 static_folder='../static')


@user.route('/')
def users_list():
    return render_template('users/users_list.html',
                           users=USERS)


@user.route('/<int:pk>/')
def user_detail(pk: int):
    if pk in USERS:
        full_name = f'{USERS[pk].get("last_name")} {USERS[pk].get("first_name")}'
        articles_id = user_articles(pk)
        return render_template('users/user_detail.html',
                               full_name=full_name,
                               articles_id=articles_id,
                               articles=ARTICLES)
    raise NotFound


def user_articles(pk: int):
    author_art = []
    for i in ARTICLES:
        if ARTICLES[i].get('article_author') == pk:
            author_art.append(i)
    return author_art
