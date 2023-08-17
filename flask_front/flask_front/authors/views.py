from flask import Blueprint, render_template
from requests import JSONDecodeError
from werkzeug.exceptions import NotFound

from flask_front.request_api.api_request import get_from_api

author = Blueprint('author',
                   __name__,
                   url_prefix='/authors',
                   )


@author.route('/')
def authors_list():

    api_path = '/api/authors/'
    m_authors_list_requests = get_from_api(api_path)
    try:
        authors = m_authors_list_requests.json()
    except JSONDecodeError:
        raise NotFound
    return render_template('authors/authors_list.html',
                           authors=authors,
                           )
