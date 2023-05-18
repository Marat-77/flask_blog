from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, \
    func
from sqlalchemy.orm import relationship

from flask_blog.models.database import db


class Article(db.Model):
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'))
    title = Column(String(200), nullable=False, default='', server_default='')
    article_text = Column(Text, nullable=False, default='', server_default='')
    created_at = Column(DateTime, default=datetime.utcnow,
                        server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    author = relationship('Author', back_populates='article')
# datetime.utcnow()
