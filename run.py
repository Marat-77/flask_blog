from flask_blog.app import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        debug=True,
        # port=8080,
        port=8090,
    )
