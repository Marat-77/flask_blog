import os

import click

from flask_blog.app import create_app
from flask_blog.models.database import db
from flask_blog.models import User, Tag

app = create_app()


# # команда создания БД
# @app.cli.command('init-db')
# def init_db():
#     db.create_all()
#     print('done! БД создана!')


# команда создания админа
@app.cli.command('create-admin')
def create_admin():
    adm_passwd = 'paranoiYa1234'
    admin = User(username='admin', is_staff=True, email='admin@test.ru')
    admin.password = os.environ.get('ADMIN_PASSWD', adm_passwd)
    db.session.add(admin)
    db.session.commit()
    print("done! Созданы администратор:", admin)


# команда создания тестовых пользователей
@app.cli.command('create-users')
def create_users():
    user1_passwd = 'paranoic123'
    user2_passwd = 'paranoic123'
    user1 = User(username='user1', first_name='Артём', last_name='Федоров',
                 email='user1@test.ru')
    user1.password = os.environ.get('ADMIN_PASSWD', user1_passwd)
    user2 = User(username='user2', first_name='Марк', last_name='Калинин',
                 email='user2@test.ru')
    user2.password = os.environ.get('ADMIN_PASSWD', user2_passwd)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    # print()
    print("done! Созданы пользователи:", user1, user2)


@app.cli.command('create-tags')
def create_tags():
    tags_ = ('python',
             'flask',
             'django',
             'fastapi',
             'sqlalchemy',
             'docker',)
    for tag_ in tags_:
        db.session.add(Tag(tag_name=tag_))
    db.session.commit()
    print(f'Теги {", ".join(tags_)} созданы')
    click.echo(f'Теги {", ".join(tags_)} созданы')
