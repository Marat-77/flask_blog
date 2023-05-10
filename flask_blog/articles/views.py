from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from flask_blog.models import User
from flask_blog.articles.mock_articles import ARTICLES
from flask_blog.users.mock_users import USERS

article = Blueprint('article',
                    __name__,
                    url_prefix='/articles',
                    static_folder='../static')


@article.route('/')
def articles_list():
    users = User.query.all()
    return render_template('articles/articles_list.html',
                           articles=ARTICLES,
                           users=users,
                           # users=USERS
                           )


@article.route('/<int:pk>/')
def article_detail(pk: int):
    users = User.query.all()
    # user = User.query.filter_by(id=pk).one_or_none()
    if pk in ARTICLES:
        user = User.query.filter_by(
            id=ARTICLES[pk]['article_author']
        ).one_or_none()
        return render_template('articles/article_detail.html',
                               # users=USERS,
                               # users=users,
                               user=user,
                               article=ARTICLES[pk])
    raise NotFound
