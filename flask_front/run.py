from flask_front.app import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080,
    )
    print('run - main - app')
else:
    print('run - main - gunicorn_app')
    print('\n!!! === GUNICORN === !!!\n')
    gunicorn_app = create_app()
