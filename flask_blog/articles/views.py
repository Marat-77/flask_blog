from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from flask_blog.articles.mock_articles import ARTICLES
from flask_blog.users.mock_users import USERS

article = Blueprint('article',
                    __name__,
                    url_prefix='/articles',
                    static_folder='../static')


@article.route('/')
def articles_list():
    return render_template('articles/articles_list.html',
                           articles=ARTICLES,
                           users=USERS)


@article.route('/<int:pk>/')
def article_detail(pk: int):
    if pk in ARTICLES:
        return render_template('articles/article_detail.html',
                               users=USERS,
                               article=ARTICLES[pk])
    raise NotFound
