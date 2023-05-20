from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from flask_blog.forms.article import CreateArticleForm
from flask_blog.models import User, Article, Author, Tag
from flask_blog.articles.mock_articles import ARTICLES
from flask_blog.models.database import db

# from flask_blog.users.mock_users import USERS

article = Blueprint('article',
                    __name__,
                    url_prefix='/articles',
                    # static_folder='../static'
                    )


@article.route('/')
def articles_list():
    try:
        users = User.query.all()
        # return render_template('articles/articles_list.html',
        #                        articles=ARTICLES,
        #                        users=users,
        #                        # users=USERS
        #                        )
    except OperationalError:
        users = None
    try:
        articles = Article.query.all()
    except OperationalError:
        articles = None
    return render_template('articles/articles_list.html',
                           articles=articles,
                           users=users,
                           )
    # users = User.query.all()
    # return render_template('articles/articles_list.html',
    #                        articles=ARTICLES,
    #                        users=users,
    #                        # users=USERS
    #                        )


@article.route('/article_create/', methods=('GET', 'POST'))
@login_required
def article_create():
    error = None
    form = CreateArticleForm(request.form)
    form.tags.choices = [
        (tag.id, tag.tag_name) for tag in Tag.query.order_by('tag_name')
    ]

    if request.method == 'POST' and form.validate_on_submit():
        article_ = Article(title=form.title.data.strip(),
                           article_text=form.article_text.data)
        db.session.add(article_)
        if current_user.author:
            article_.author = current_user.author
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article_.author = current_user.author
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article_.tags.append(tag)
        try:
            db.session.commit()
        except IntegrityError:
            error = 'ОШИБКА: статья не создана'
        else:
            return redirect(url_for('article.article_detail',
                                    pk=article_.id))
    return render_template('articles/article_create.html',
                           form=form, error=error)


@article.route('/<int:pk>/')
def article_detail(pk: int):
    article_ = Article.query.filter_by(id=pk).options(
        joinedload(Article.tags)
    ).one_or_none()
    if article_ is None:
        raise NotFound
    try:
        author = User.query.filter_by(
            id=article_.author_id
        ).one_or_none()
        # user = User.query.filter_by(
        #     id=article_.author_id
        # ).one_or_none()
    except OperationalError:
        # user = None
        author = None
    return render_template('articles/article_detail.html',
                           # user=user,
                           # author=author,
                           article=article_)
    # # -----------------------------------
    # # users = User.query.all()
    # # user = User.query.filter_by(id=pk).one_or_none()
    # if pk in ARTICLES:
    #     try:
    #         user = User.query.filter_by(
    #             id=ARTICLES[pk]['article_author']
    #         ).one_or_none()
    #     except OperationalError:
    #         user = None
    #     return render_template('articles/article_detail.html',
    #                            user=user,
    #                            article=ARTICLES[pk])
    # raise NotFound

    # try:
    #     users = User.query.all()
    #     if pk in ARTICLES:
    #         user = User.query.filter_by(
    #             id=ARTICLES[pk]['article_author']
    #         ).one_or_none()
    #         return render_template('articles/article_detail.html',
    #                                # users=USERS,
    #                                # users=users,
    #                                user=user,
    #                                article=ARTICLES[pk])
    #     raise NotFound
    # except OperationalError:
    #     raise NotFound
    # users = User.query.all()
    # # user = User.query.filter_by(id=pk).one_or_none()
    # if pk in ARTICLES:
    #     user = User.query.filter_by(
    #         id=ARTICLES[pk]['article_author']
    #     ).one_or_none()
    #     return render_template('articles/article_detail.html',
    #                            # users=USERS,
    #                            # users=users,
    #                            user=user,
    #                            article=ARTICLES[pk])
    # raise NotFound
