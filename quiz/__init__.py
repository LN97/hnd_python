import random

from flask_admin import Admin
from flask import Flask, render_template, jsonify, session, redirect
from flask_security import Security, SQLAlchemyUserDatastore, utils


from quiz.views import *
from quiz.models import *

def create_app(config=None, env=None):
  app = Flask(__name__)
  app.config.from_object('config')

  db.init_app(app)

  users_ds = SQLAlchemyUserDatastore(db, User, Role)
  security = Security(app, users_ds)

  admin = Admin(
    app, 'Quiz', base_template='',
    index_view=UserView(User, db.session, url='/admin'),
    template_mode='bootstrap3'
  )

  admin.add_view(QuestionView(Question, db.session, url='/admin/question'))
  admin.add_view(AnswerView(Answer, db.session, url='/admin/Answer'))

  @app.route('/')
  def root():
    return render_template('index.html')

  @app.route('/game')
  def game():
    session['score'] = 0
    return redirect('/game/1', 302)


  @app.route('/answer/<int:qid>/<int:aid>')
  def answer(qid, aid):
    if 'score' not in session:
      session['score'] = 0

    q = Question.query.filter_by(id=qid).all()

    if len(q) < 1:
      return jsonify({"err": "Invalid question id"})

    q = q[0]

    a = Answer.query.filter_by(id=aid).all()
    if len(a) < 1:
      return jsonify({"err": "Invalid answer id"})
    
    if a[0].correct:
      session['score'] += 10

    return jsonify({"correct":  a[0].correct})

  @app.route('/game/<int:idx>')
  def gamebyid(idx):
    if 'score' not in session:
      session['score'] = 0

    q = Question.query.filter_by(id=idx).all()[0]
    a = q.answers
    random.shuffle(a)
    return render_template('game.html', question = q, answers = a, score = session['score'])

  @app.before_first_request
  def before_first_request():
    print("[*] Migrating database ")
    db.drop_all()
    print("[DB]: Cleaned up")
    db.create_all()
    print("[DB]: Schema deployed")

    users_ds.find_or_create_role(name='admin', description='Administrator')
    users_ds.find_or_create_role(name='user', description='user')

    password = utils.hash_password(config.SECRET_KEY)
    users_ds.create_user(email='admin@admin.admin', password=password)

    db.session.commit()

    # Add admin role to user
    users_ds.add_role_to_user('admin@admin.admin', 'admin')
    db.session.commit()

    # Load questions and correct answers from file
    q = [Question(body=q) for q in open("q.txt", "r").read().splitlines()]
    a = [Answer(body=a, correct=True) for a in open("a.txt", "r").read().splitlines()]

    for question in q:
      db.session.add(question)

    db.session.commit()

    for answer in a:
      db.session.add(answer)
      q[a.index(answer)].answers.append(answer)


    db.session.commit()

    # Load false answers from file

    for l in open("f.txt", "r").read().splitlines():
      data = l.split(",")
      answers = [Answer(body=a, correct=False) for a in data[0:3]]
      for a in answers:
        db.session.add(answer)
        q[int(data[3])-1].answers.append(a)


    db.session.commit()


  return app
