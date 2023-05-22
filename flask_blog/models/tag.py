from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from flask_blog.models.article_tag import article_tag_associated_table
from flask_blog.models.database import db


class Tag(db.Model):
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(64), unique=True, nullable=False)
    articles = relationship('Article',
                            secondary=article_tag_associated_table,
                            back_populates='tags')
