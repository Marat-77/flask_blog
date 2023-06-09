from flask_restx import Namespace, Resource

from flask_blog.api.schemas import user_schema, author_schema, article_schema
from flask_blog.models import User, Author, Article

ns = Namespace("api")


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
    @ns.marshal_list_with(user_schema)
    def get(self):
        return User.query.all()


@ns.route('/authors')
class AuthorsAPI(Resource):
    @ns.marshal_list_with(author_schema)
    def get(self):
        return Author.query.all()


@ns.route('/articles')
class ArticlesAPI(Resource):
    @ns.marshal_list_with(article_schema)
    def get(self):
        return Article.query.all()


@ns.route('/hello')
class Hello(Resource):
    def get(self):
        return {"hello": "restx"}
