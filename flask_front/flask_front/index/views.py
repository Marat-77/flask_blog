from flask import Blueprint, render_template

from flask_front.request_api.api_request import get_from_api

index = Blueprint('index',
                  __name__,
                  url_prefix='/',
                  )


@index.route('/')
def index_():
    api_path_index = '/api/'
    api_index = get_from_api(api_path_index)
    rrr, api_url = api_index

    return render_template('index.html',
                           api_url=api_url)
