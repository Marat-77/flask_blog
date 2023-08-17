from flask import Blueprint, render_template

error_ = Blueprint('errors',
                   __name__,
                   static_folder='../static')


@error_.app_errorhandler(404)
def not_found(err):
    return render_template('err404.html'), 404
