import pytest

from flask_blog.api import create_app


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


def test_get_api_index(client):
    # http://127.0.0.1:8090/api/
    response = client.get('/api/')
    assert response.status_code == 200
    assert response.json['title'] == 'Главная страница'


def test_get_api_articles(client):
    # http://127.0.0.1:8090/api/articles/
    response = client.get('/api/articles')
    assert response.status_code == 200
    assert 'article_text' in response.json[0]


def test_get_api_users(client):
    # http://127.0.0.1:8090/api/users/
    response = client.get('/api/users')
    assert response.status_code == 401


def test_get_api_authors(client):
    # http://127.0.0.1:8090/api/authors/
    response = client.get('/api/authors')
    assert response.status_code == 200


def test_get_api_author(client):
    # http://127.0.0.1:8090/api/authors/1
    response = client.get('/api/authors/1')
    assert response.status_code == 200


# def test_get_auth_register(client):
#     # http://127.0.0.1:8090/auth/register/
#     response = client.get('/auth/register/')
#     assert response.status_code == 200
#     assert '<h1>Регистрация</h1>' in response.text
#
#
# def test_get_auth_login(client):
#     # http://127.0.0.1:8090/auth/login/
#     response = client.get('/auth/login/')
#     assert response.status_code == 200
#     assert '<h1>Вход</h1>' in response.text
#
