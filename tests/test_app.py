import pytest

from flask_blog.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_get_index(client):
    # http://127.0.0.1:8090/
    response = client.get('/')
    assert response.status_code == 200


def test_get_articles(client):
    # http://127.0.0.1:8090/articles/
    response = client.get('/articles/')
    assert response.status_code == 200
    # assert '<h1>Статьи:</h1>' in str(response.data.decode('utf-8'))
    assert '<h1>Статьи:</h1>' in response.text


def test_get_users(client):
    # http://127.0.0.1:8090/users/
    response = client.get('/users/')
    assert response.status_code == 200
    assert '<h1>Список пользователей:</h1>' in response.text


def test_get_authors(client):
    # http://127.0.0.1:8090/authors/
    response = client.get('/authors/')
    assert response.status_code == 200
    assert '<h1>Список авторов:</h1>' in response.text


def test_get_auth_register(client):
    # http://127.0.0.1:8090/auth/register/
    response = client.get('/auth/register/')
    assert response.status_code == 200
    assert '<h1>Регистрация</h1>' in response.text


def test_get_auth_login(client):
    # http://127.0.0.1:8090/auth/login/
    response = client.get('/auth/login/')
    assert response.status_code == 200
    assert '<h1>Вход</h1>' in response.text
#
