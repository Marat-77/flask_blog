from flask import Blueprint, render_template
from sqlalchemy.exc import OperationalError

from flask_blog.models import Author

author = Blueprint('author',
                   __name__,
                   url_prefix='/authors',
                   )


@author.route('/')
def authors_list():
    try:
        authors = Author.query.all()
    except OperationalError:
        authors = None
    return render_template('authors/authors_list.html',
                           authors=authors,
                           )
