import os

import click
from sqlalchemy.exc import IntegrityError

from flask_backend.api import create_app
from flask_backend.models.database import db
from flask_backend.models import User  # , Tag

app = create_app()


# команда создания админа
@app.cli.command('create-admin')
@click.argument('adm_email', envvar='ADMIN_EMAIL')
@click.argument('adm_passwd', envvar='ADMIN_PASSWD')
def create_admin(adm_email=None, adm_passwd=None):
    """
    Create admin.
    Without arguments - you need environments ADMIN_EMAIL and ADMIN_PASSWD.
    :param adm_email: admin email
    :param adm_passwd: admin password
    """
    if adm_email is None or adm_passwd is None:
        click.echo('Администратор не создан')
    else:
        admin = User(username='admin', is_staff=True)
        admin.password = adm_passwd
        admin.email = adm_email
        db.session.add(admin)
        try:
            db.session.commit()
        except IntegrityError as err:
            click.echo(err)
            click.echo(f'Администратор с таким email ({adm_email}) уже создан')
        except Exception as err:
            click.echo(err)
            click.echo('Что-то пошло не так')
        else:
            click.echo(f"done! Создан администратор: {admin.email}")
