from sqlalchemy import Table, Column, Integer, ForeignKey

from flask_backend.models.database import db

article_tag_associated_table = Table(
    'article_tag_associated',
    db.metadata,
    Column('article_id', Integer, ForeignKey('article.id'), nullable=False),
    Column('tag_id', Integer, ForeignKey('tag.id'), nullable=False),
)

