from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()


roles_users = db.Table(
  'roles_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
  db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

answers_questions = db.Table(
  'answers_questions',
  db.Column('question_id', db.Integer(), db.ForeignKey('question.id')),
  db.Column('answer_id', db.Integer(), db.ForeignKey('answer.id')),
)


class Role(db.Model, RoleMixin):
  id          = db.Column(db.Integer, primary_key = True, unique = True)
  name        = db.Column(db.String(80), unique   = True)
  description = db.Column(db.String(255))

class User(db.Model, UserMixin):
  id       = db.Column(db.Integer, primary_key = True, unique = True)
  email    = db.Column(db.String(255), unique  = True)
  password = db.Column(db.String(255))
  active   = db.Column(db.Boolean())
  roles    = db.relationship(
    'Role',
    secondary = roles_users,
    backref = db.backref('users', lazy = 'dynamic')
  )

class Answer(db.Model):
  id       = db.Column(db.Integer, primary_key = True, unique = True)
  correct  = db.Column(db.Boolean)
  body     = db.Column(db.String(255), unique = True)

class Question(db.Model):
  id       = db.Column(db.Integer, primary_key = True, unique = True)
  body     = db.Column(db.String(255), unique = True)
  answers  = db.relationship(
    'Answer',
    secondary = answers_questions,
    backref = db.backref('questions', lazy = 'dynamic')
  )
