from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean

from flask_blog.models.database import db


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(155), unique=True, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    first_name = Column(String(155), nullable=True)
    last_name = Column(String(155), nullable=True)
    email = Column(String(255), nullable=False, default="", server_default="")

    def __repr__(self):
        return f'<User #{self.id} {self.username}>'

