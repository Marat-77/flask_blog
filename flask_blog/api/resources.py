from flask_jwt_extended import jwt_required, get_jwt_identity, \
    create_access_token
from flask_restx import Namespace, Resource

from flask_blog.api.schemas import user_schema, author_schema, article_schema, \
    login_schema, register_schema
from flask_blog.models import User, Author, Article
from flask_blog.models.database import db

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


@ns.route('/users')
class UsersAPI(Resource):
    method_decorators = [jwt_required()]
    # Bearer token

    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(user_schema)
    def get(self):
        print(get_jwt_identity())
        return User.query.all()


@ns.route('/users/<int:id>')
class UserAPI(Resource):
    @ns.marshal_with(user_schema)
    def get(self, id):
        return User.query.get(id)


@ns.route('/authors')
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
        # articles_count = Article.query.count()
        return {"articles count": Article.query.count()}


@ns.route('/articles')
class ArticlesAPI(Resource):
    @ns.marshal_list_with(article_schema)
    def get(self):
        return Article.query.all()


@ns.route('/articles/<int:pk>')
class ArticleAPI(Resource):
    @ns.marshal_with(article_schema)
    def get(self, pk):
        article = Article.query.get(pk)
        # print(f'Article {pk}:', article, article is None)
        if article is None:
            # print(f'Article {pk} -', article is None)
            return {"message": "Not found"}, 404
        return article, 200


@ns.route('/register')
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
        db.session.commit()
        return user, 201


@ns.route('/login')
class Login(Resource):

    @ns.expect(login_schema)
    def post(self):
        user = User.query.filter_by(username=ns.payload['username']).first()
        if not user:
            return {'error': 'пользователь не найден'}, 401
        if not user.validate_password(ns.payload['password']):
            return {'error': 'Неверное имя пользователя или пароль'}, 401
        return {'access_token': create_access_token(user.username)}
