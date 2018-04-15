from flask import url_for, redirect, request
from flask_admin.model import template
from flask_security import current_user
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView, typefmt
from flask_admin import BaseView, expose
from datetime import datetime

class UserView(ModelView):

  def is_accessible(self):
    return current_user.is_authenticated and current_user.has_role('admin')

  def inaccessible_callback(self, name, **kwargs):
    if current_user.is_authenticated:
      return 'Not an ADMIN'
    else:
      return redirect(url_for('security.login', next=request.path[1:-1]))

  column_sortable_list = ('email', 'password')

  form_base_class = SecureForm
  form_excluded_columns = ["created", "updated"]

  edit_modal = True
  page_size  = 10

  column_searchable_list = ['email', 'password']
  can_export = True

  def __init__(self, model, session, *args, **kwargs):
    super(UserView, self).__init__(model, session, *args, **kwargs)
    self.static_folder = 'static'
    self.endpoint = 'admin'
    self.name = 'Users'

class QuestionView(ModelView):

  def is_accessible(self):
    return True

  def inaccessible_callback(self, name, **kwargs):
    if current_user.is_authenticated:
      return 'not an admin'
    else:
      return redirect(url_for('security.login', next=request.path[1:-1]))

  column_hide_backrefs = False

  column_sortable_list = ('id', 'body', 'answers')
  column_list = ('id', 'body', 'answers')

  form_base_class = SecureForm

  edit_modal = True
  page_size  = 10

  column_searchable_list = ['id', 'body']
  can_export = True

  def __init__(self, model, session, *args, **kwargs):
    super(QuestionView, self).__init__(model, session, *args, **kwargs)
    self.static_folder = 'static'
    self.endpoint = 'admin/question'
    self.name = 'questions'

class AnswerView(ModelView):

  def is_accessible(self):
    return True

  def inaccessible_callback(self, name, **kwargs):
    if current_user.is_authenticated:
      return 'not an admin'
    else:
      return redirect(url_for('security.login', next=request.path[1:-1]))

  column_sortable_list = ('id', 'body', 'correct')
  column_list = ('id', 'body', 'correct')

  form_base_class = SecureForm

  edit_modal = True
  page_size  = 10

  column_searchable_list = ['id', 'body', 'correct']
  can_export = True

  def __init__(self, model, session, *args, **kwargs):
    super(AnswerView, self).__init__(model, session, *args, **kwargs)
    self.static_folder = 'static'
    self.endpoint = 'admin/answer'
    self.name = 'answer'
