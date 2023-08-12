from flask import Blueprint, render_template, request, session
from flask_login import login_required
from requests import JSONDecodeError
from werkzeug.exceptions import NotFound

from flask_front.request_api.api_request import get_from_api, post_to_api

user = Blueprint('user',
                 __name__,
                 url_prefix='/users',
                 )


@user.route('/')
@login_required
def users_list():
    # get an access_token with refresh_token
    api_path_refresh = '/api/refresh'
    token_headers = dict(request.headers)
    get_refresh_token = session.get('_refresh_token')
    token_headers['Authorization'] = f'Bearer {get_refresh_token}'
    token_payload = {'refresh_token': get_refresh_token}
    token_request = post_to_api(api_path_refresh,
                                token_payload,
                                headers_=token_headers)
    get_token = token_request.json()
    access_token = get_token.get('access_token')
    refresh_token = get_token.get('refresh_token')
    if refresh_token is not None:
        session['_refresh_token'] = refresh_token
    headers = dict(request.headers)
    headers['Authorization'] = f'Bearer {access_token}'
    api_path_users = '/api/users/'
    users_request = get_from_api(api_path_users, headers_=headers)
    try:
        if not users_request.ok:
            raise NotFound
        users = users_request.json()
        return render_template('users/users_list.html',
                               users=users,
                               )
    except JSONDecodeError:
        raise NotFound


@user.route('/<int:pk>/')
@login_required
def user_detail(pk: int):
    api_path = f'/api/users/{pk}'
    m_authors_list_requests = get_from_api(api_path)
    try:
        user_pk = m_authors_list_requests.json()

        return render_template('users/user_detail.html',
                               user=user_pk,
                               )
    except JSONDecodeError:
        raise NotFound
