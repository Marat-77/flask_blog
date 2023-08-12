from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, \
    session
from flask_login import current_user, login_required
# import requests
from requests import JSONDecodeError
# from sqlalchemy.exc import OperationalError, IntegrityError
# from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound, RequestTimeout

from flask_front.forms.article import CreateArticleForm
from flask_front.request_api.api_request import get_from_api, post_to_api


article = Blueprint('article',
                    __name__,
                    url_prefix='/articles',
                    )


@article.route('/')
def articles_list():
    print('\n !!! articles_list !!!')

    api_articles_count = '/api/articles/count'
    api_path_articles = '/api/articles/'
    api_articles = get_from_api(api_path_articles)
    api_articles_count = get_from_api(api_articles_count)
    try:
        articles = api_articles.json()
        articles_count = api_articles_count.json()
        articles_count = articles_count.get('articles count')
    except Exception as err:
        print('articles_list error:', err)
        raise NotFound
    else:
        return render_template('articles/articles_list.html',
                               articles=articles,
                               articles_count=articles_count,
                               # users=users,
                               )


@article.route('/article_create/', methods=('GET', 'POST'))
@login_required
def article_create():
    error = None
    form = CreateArticleForm(request.form)
    api_path = '/api/tags'
    tag_request = get_from_api(api_path)
    try:
        tag_request = tag_request.json()
        form.tags.choices = [
            (tag.get('id'), tag.get('tag_name')) for tag in tag_request
        ]
    except JSONDecodeError:
        raise NotFound

    if request.method == 'POST' and form.validate_on_submit():
        api_path_refresh = '/api/refresh'
        token_headers = dict(request.headers)
        get_refresh_token = session.get('_refresh_token')
        token_headers['Authorization'] = f'Bearer {get_refresh_token}'
        token_payload = {'refresh_token': get_refresh_token}
        token_request = post_to_api(api_path_refresh, token_payload,
                                    token_headers)
        get_token = token_request.json()
        access_token = get_token.get('access_token')
        refresh_token = get_token.get('refresh_token')
        if refresh_token is not None:
            session['_refresh_token'] = refresh_token
        headers = dict(request.headers)
        headers['Authorization'] = f'Bearer {access_token}'
        api_path_create_article = '/api/articles/'
        payload = {'title': form.title.data,
                   'article_text': form.article_text.data,
                   'tags': form.tags.data}
        create_article_request = post_to_api(api_path_create_article,
                                             to_api_payload=payload,
                                             headers_=headers)
        return redirect(url_for('article.articles_list'))
    return render_template('articles/article_create.html',
                           form=form,
                           error=error
                           )


@article.route('/<int:pk>/')
def article_detail(pk: int):
    api_path = f'/api/articles/{pk}'
    r = get_from_api(api_path)
    if not r.ok:
        raise NotFound
    article_ = r.json()
    # print(article_['updated_at'])
    updated_at = article_['updated_at']
    if updated_at is None:
        updated_at = article_['created_at']
    dt = datetime.fromisoformat(updated_at)
    delta_msk = timedelta(hours=3)
    dt += delta_msk
    dt_format = '%d.%m.%Y %H:%M'
    article_['updated_at'] = f'{datetime.strftime(dt, dt_format)} (МСК)'
    return render_template('articles/article_detail.html',
                           article=article_)
