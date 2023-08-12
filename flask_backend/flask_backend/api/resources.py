# import time

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, \
    create_access_token, create_refresh_token, get_current_user, \
    verify_jwt_in_request
from flask_restx import Namespace, Resource
from sqlalchemy.exc import IntegrityError

from flask_backend.api.schemas import user_schema, author_schema, \
    article_schema, login_schema, register_schema, tag_schema, \
    article_schema_post, refresh_schema
from flask_backend.models import User, Author, Article, Tag
from flask_backend.models.database import db

authorizations = {
    'jsonWebToken': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
ns = Namespace("api", authorizations=authorizations)


@ns.route('/')
class IndexApi(Resource):
    def get(self):
        text = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. ' \
               'Aspernatur autem beatae consequuntur culpa debitis dicta ' \
               'distinctio, eveniet fugit id in iure laborum magni molestiae ' \
               'nihil, odio perspiciatis placeat, praesentium quod suscipit ' \
               'voluptates. Ad asperiores deleniti, dolores expedita ' \
               'recusandae rerum vero voluptatum! Atque cupiditate enim ' \
               'eveniet fugiat magnam molestiae nisi nobis pariatur ' \
               'provident velit. Ab aliquid aut, blanditiis dolores esse ' \
               'fugit iste, iure, natus nihil quisquam quo ratione soluta ' \
               'tempore ullam veritatis! At nostrum reprehenderit sint ' \
               'vitae. A aperiam architecto assumenda corporis cum, delectus ' \
               'doloremque ea hic inventore iusto laborum natus nulla optio ' \
               'perferendis qui quis recusandae repudiandae vitae. ' \
               'Necessitatibus neque saepe tempore. Aspernatur dicta nisi ' \
               'nulla vel voluptate? Atque blanditiis debitis doloremque ' \
               'dolores doloribus eius eveniet exercitationem illo illum, ' \
               'inventore ipsam iusto laudantium, minus odio possimus qui ' \
               'reiciendis velit? Beatae, ea earum esse est ex excepturi id ' \
               'minima natus possimus reiciendis repellat veniam. Accusamus ' \
               'aperiam commodi et harum, molestiae nihil?'
        return {'title': 'Главная страница',
                'content': text}


@ns.route('/users/')
class UsersAPI(Resource):
    method_decorators = [jwt_required()]

    # Bearer token

    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(user_schema)
    def get(self):
        return User.query.all()


@ns.route('/users/<int:id>')
class UserAPI(Resource):
    @ns.marshal_with(user_schema)
    def get(self, id):
        user_ = User.query.get(id)
        return user_


@ns.route('/authors/')
class AuthorsAPI(Resource):
    @ns.marshal_list_with(author_schema)
    def get(self):
        return Author.query.all()


@ns.route('/authors/<int:id>')
class AuthorAPI(Resource):
    @ns.marshal_with(author_schema)
    def get(self, id):
        return Author.query.get(id)


@ns.route('/articles/count')
class ArticlesCount(Resource):
    def get(self):
        return {"articles count": Article.query.count()}


@ns.route('/articles/')
class ArticlesAPI(Resource):

    @ns.doc(security='jsonWebToken')
    @ns.expect(article_schema_post)
    @ns.marshal_with(article_schema)
    @jwt_required()
    def post(self):
        article_ = Article()
        article_.title = ns.payload['title']
        article_.article_text = ns.payload['article_text']
        selected_tags = ns.payload['tags']
        author_get_jwt_identity = get_jwt_identity()
        user_ = db.session.query(User).filter_by(
            username=author_get_jwt_identity
        ).first()
        author = Author(user_id=user_.id)
        article_.author = author
        if selected_tags:
            tags_ = db.session.query(Tag).filter(Tag.id.in_(selected_tags))
            for tag in tags_:
                article_.tags.append(tag)
        db.session.add(article_)
        try:
            db.session.commit()
        except IntegrityError:
            error = 'ОШИБКА: статья не создана'
        else:
            return article_, 201

        return {'error': error}, 409

    @ns.marshal_list_with(article_schema)
    def get(self):
        return Article.query.all()


@ns.route('/articles/<int:pk>')
class ArticleAPI(Resource):
    @ns.marshal_with(article_schema)
    def get(self, pk):
        article = Article.query.get(pk)
        if article is None:
            return {"message": "Not found"}, 404
        return article, 200


@ns.route('/tags/')
class TagsAPI(Resource):
    @ns.marshal_list_with(tag_schema)
    def get(self):
        db_session_query_tag = db.session.query(Tag).order_by('tag_name').all()
        return db_session_query_tag, 200


@ns.route('/register/')
class Register(Resource):
    @ns.expect(register_schema)
    @ns.marshal_with(user_schema)
    def post(self):
        user = User(username=ns.payload['username'],
                    first_name=ns.payload['first_name'],
                    last_name=ns.payload['last_name'],
                    email=ns.payload['email'],
                    is_staff=False)
        user.password = ns.payload['password']
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError as err:
            print('error:', err)
            return {'error': 'username или email уже используется'}, 409

        return user, 201


@ns.route('/login/')
class Login(Resource):

    @ns.expect(login_schema)
    def post(self):
        user = db.session.query(User).filter_by(
            username=ns.payload['username']
        ).first()
        if not user:
            return {'error': 'пользователь не найден'}, 401
        if not user.validate_password(ns.payload['password']):
            return {'error': 'Неверное имя пользователя или пароль'}, 401
        access_token = create_access_token(user.username, fresh=True)
        refresh_token = create_refresh_token(user.username)
        api_user = {'user_id': user.id, 'username': user.username}
        return {'access_token': access_token,
                'refresh_token': refresh_token,
                'user': api_user}, 200


@ns.route('/refresh')
class RefreshToken(Resource):

    @ns.expect(refresh_schema)
    @jwt_required(refresh=True)
    def post(self):
        user_get_jwt_identity = get_jwt_identity()
        user_ = db.session.query(User).filter_by(
            username=user_get_jwt_identity
        ).first()
        access_token = create_access_token(user_.username, fresh=True)
        refresh_token = create_refresh_token(user_.username)
        return {'access_token': access_token,
                'refresh_token': refresh_token}, 200
