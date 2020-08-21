import secrets
import os
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('Your account has been created! You are now able to log in', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('index'))
    else:
      flash('Cannot find account, please check your email and password', 'danger')  
  return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))



def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  _, file_extension = os.path.splitext(form_picture.filename)
  picture_filename = random_hex + file_extension
  picture_path = os.path.join(app.root_path, 'static/profile-pics', picture_filename)

  output_size = (125,125)
  scaled_image = Image.open(form_picture)
  scaled_image.thumbnail(output_size)

  scaled_image.save(picture_path)
  return picture_filename

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated', 'success')
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email 
  image_file = url_for('static', filename='profile-pics/' + current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form)