from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, \
    SelectMultipleField
from wtforms.validators import DataRequired, Length


class CreateArticleForm(FlaskForm):
    title = StringField('Заголовок', [DataRequired(),
                                      Length(max=200)])
    article_text = TextAreaField('Текст статьи', [DataRequired()])
    tags = SelectMultipleField('Теги', coerce=int)
    submit = SubmitField('Опубликовать')
