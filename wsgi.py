from flask_blog.app import create_app
from flask_blog.models.database import db
from flask_blog.models import User


app = create_app()


# команда создания БД
@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('done! БД создана!')


# команда создания тестовых пользователей
@app.cli.command('create-users')
def create_users():
    admin = User(username='admin', is_staff=True)
    user1 = User(username='user1', first_name='Артём', last_name='Федоров')
    db.session.add(admin)
    db.session.add(user1)
    db.session.commit()
    print()
    print("done! Созданы пользователи:", admin, user1)
