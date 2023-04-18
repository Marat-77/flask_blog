from flask import Blueprint, render_template

error_ = Blueprint('errors',
                   __name__,
                   static_folder='../static')


@error_.app_errorhandler(404)
def not_found(err):
    return render_template('err404.html'), 404

# bp = Blueprint('errors', __name__)
#
# @bp.app_errorhandler(404)
# def handle_404(err):
#     return render_template('404.html'), 404
#
# @bp.app_errorhandler(500)
# def handle_500(err):
#     return render_template('500.html'), 500