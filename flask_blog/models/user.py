from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary

from flask_blog.models.database import db
from flask_blog.security import blog_bcrypt


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(155), unique=True, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    first_name = Column(String(155), nullable=True)
    last_name = Column(String(155), nullable=True)
    email = Column(String(255), unique=True, nullable=False,
                   default="", server_default="")
    _password = Column(LargeBinary, nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = blog_bcrypt.generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return blog_bcrypt.check_password_hash(self._password, password)

    def __repr__(self):
        return f'<User #{self.id} {self.username}>'

