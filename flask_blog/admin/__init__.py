# def register_views():
#     from flask_blog import models
#     from flask_blog.admin.views import TagAdminView, ArticleAdminView, UserAdminView
#     from flask_blog.extensions import admin, db
#
#     admin.add_view(ArticleAdminView(models.Article, db.session, category='Models'))
#     admin.add_view(TagAdminView(models.Tag, db.session, category='Models'))
#     admin.add_view(UserAdminView(models.User, db.session, category='Models'))
# from flask_admin import Admin
#
# from flask_blog.admin.views import CustomAdminIndexView
#
# admin = Admin(index_view=CustomAdminIndexView(), name='Blog_Admin', template_mode='bootstrap4')
# class CustomAdminIndexView:
#     pass

from flask_blog.admin.views import (CustomAdminView, CustomAdminIndexView,
                                    TagAdminView, ArticleAdminView,
                                    UserAdminView)


__all__ = [
    'CustomAdminView',
    'CustomAdminIndexView',
    'TagAdminView',
    'ArticleAdminView',
    'UserAdminView'
]