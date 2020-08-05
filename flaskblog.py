from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f51a65e22d77a2e355ac3bd244268011'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAllchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True ,nullable=False)
  email = db.Column(db.String(120), unique=True ,nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  password = db.Column(db.String(60), nullable=False)
  posts = db.relationship('Post', backref='author', lazy=True)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  content = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return f"User('{self.title}', '{self.date_posted}')"



# dummy data
posts = [
  {
    'author': 'Ryan Adi Putra',
    'title': 'Blogpost 1',
    'content': 'First post content',
    'date_posted': 'July 31, 2020'
  },
  {
    'author': 'Bogel',
    'title': 'Blogpost 2',
    'content': 'Second post content',
    'date_posted': 'August 1, 2020'
  }
]


@app.route('/')
@app.route('/home')
def index():
  return render_template('index.html', posts=posts)

@app.route('/about')
def about():
  return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('index'))

  return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
      flash('You have been logged in', 'success')
      return redirect(url_for('index'))
    flash('Cannot find account, please check your email and password', 'danger')  
  return render_template('login.html', title='Login', form=form)



if __name__ == '__main__':
  app.run(debug=True)