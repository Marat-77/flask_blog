from flask_restx import fields

from flask_blog.api import api

user_schema = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
})

author_schema = api.model('Author', {
    'id': fields.Integer,
    'user': fields.Nested(user_schema),
})

article_schema = api.model('Article', {
    'id': fields.Integer,
    'title': fields.String,
    'article_text': fields.String,
    'author': fields.Nested(author_schema)
})
