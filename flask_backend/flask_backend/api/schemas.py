from flask_restx import fields

from flask_backend.api import api

# user_article_schema = api.model('UserArticles', {
#     'id': fields.Integer,
#     'title': fields.String
# })

# # UserAuthorArticle
user_author_articles_schema = api.model('UserAuthorArticle', {
    'id': fields.Integer,
    'title': fields.String
})

user_author_schema = api.model('AuthorUser', {
    'id': fields.Integer,
    'article': fields.List(fields.Nested(user_author_articles_schema))
})

user_schema = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    # 'author': fields.String,
    'author': fields.Nested(user_author_schema),
    'email': fields.String,
    # 'articles': fields.Nested(user_article_schema),
})

author_schema = api.model('Author', {
    'id': fields.Integer,
    'user': fields.Nested(user_schema),
})

tag_schema = api.model('Tag', {
    'id': fields.Integer,
    'tag_name': fields.String
})

article_schema = api.model('Article', {
    'id': fields.Integer,
    'title': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'article_text': fields.String,
    'author': fields.Nested(author_schema),
    'tags': fields.Nested(tag_schema)
})

# author_schema = api.model('AuthorArticles', {
#     'id': fields.Integer,
#     'article': fields.Nested(user_schema),
# })

article_schema_post = api.model('ArticlePost', {
    'title': fields.String,
    'article_text': fields.String,
    'tags': fields.List(fields.Integer)
})

register_schema = api.model('RegisterModel', {
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password': fields.String
})

login_schema = api.model('LoginModel', {
    'username': fields.String,
    'password': fields.String
})

refresh_schema = api.model('RefreshModel', {
    'refresh_token': fields.String
})
