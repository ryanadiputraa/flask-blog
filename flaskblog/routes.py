from flask import render_template, flash, redirect, url_for
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

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