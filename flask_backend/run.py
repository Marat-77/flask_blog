from flask_backend.api import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5050,
    )
    print('run - main - app')
else:
    print('\n!!! run - main - gunicorn_app !!!\n')
    gunicorn_app = create_app()

