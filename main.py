from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, CommentForm, CreatePostForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_gravatar import Gravatar
from functools import wraps
from flask import abort
import os
import random
import datetime
import requests



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='intro')

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL",  "sqlite:///blog.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLES

class NewPatient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer)
    # Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    # author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    patient_name = db.Column(db.String(250), nullable=False)
    patient_age = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    #***************Parent Relationship*************#
    # comments = relationship("Comment", back_populates="parent_post")

db.create_all()


# Create the User Table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    patient_contact = db.Column(db.Integer, primary_key=True)
    patient_age = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), unique=True)
    facility = db.Column(db.String(100), unique=True)
    unit = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    #This will act like a List of NewPatient objects attached to each User.
    #The "author" refers to the author property in the NewPatient class.
    posts = relationship("NewPatient", back_populates="author")

    #*******Add parent relationship*******#
    #"comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")

# Create all the tables in the database
db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/')
def get_all_patients():
    posts = NewPatient.query.all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route('/sample')
def sample():
    random_number = random.randint(1, 20)
    answer = random_number * 2
    current_year = datetime.datetime.now().year
    return render_template('web.html', response=random_number, num=answer, year=current_year)

@app.route('/guess/<name>')
def guess(name):
    gender_url = f'https://api.genderize.io?name={name}'
    gender_response = requests.get(gender_url)
    gender_data = gender_response.json()
    gender = gender_data['gender']
    age_url = f'https://api.agify.io?name={name}'
    age_response = requests.get(age_url)
    age_data = age_response.json()
    age = age_data['age']
    current_year = datetime.datetime.now().year
    return render_template('guess.html', person_name=name, gender=gender, age=age, year=current_year)


@app.route('/blog')
def blog():

    return render_template('blog.html')


@app.route('/wounds', methods=["GET"])
def woundcare():

    return render_template('woundcare.html')

@app.route('/', methods=['GET'])
def dropdown():
    extent_of_tissue = ['cough', 'Enviromental_Factors', 'Dysponia', 'Catarrh'
                        ' Cyanosis', ' Psychological_Factors', ' Smoking',
                        'Nose Pains', 'Chest X-ray', 'Chest Pain']
    return render_template('woundcare.html', colours=extent_of_tissue)

@app.route("/new-patient", methods=["GET", "POST"])
def add_new_patient():
    post = RegisterForm()
    if post.validate_on_submit():
        new_post = NewPatient(
            title=post.title.data,
            patient_name=post.patient_name.data,
            patient_age=post.patient_age.data,
            unit=post.unit.data,
            facility=post.facility.data,
            body=post.body.data,
            img_url=post.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_patients"))
    return render_template("create_patient.html", post=post, current_user=current_user)


@app.route("/edit-post/<int:patient_id>", methods=["GET", "POST"])
def edit_patient(patient_id):
    post = NewPatient.query.get(patient_id)
    edit_patient = RegisterForm(
        patient_name=post.patient_name,
        patient_age=post.patient_age,
        unit=post.unit,
        facility=post.facility,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_patient.validate_on_submit():
        post.title = edit_patient.title.data
        post.subtitle = edit_patient.subtitle.data
        post.img_url = edit_patient.img_url.data
        post.author = edit_patient.author.data
        post.body = edit_patient.body.data
        db.session.commit()
        return redirect(url_for("show_patient", patient_id=post.id))

    return render_template("create_patient.html", form=edit_patient, is_edit=True, current_user=current_user)




# @app.route("/post/<int:post_id>", methods=["GET", "POST"])
# def show_patient(post_id):
#     form = CommentForm()
#     requested_post = NewPatient.query.get(post_id)
#
#     if form.validate_on_submit():
#         if not current_user.is_authenticated:
#             flash("You need to login or register to comment.")
#             return redirect(url_for("login"))
#
#         new_comment = Comment(
#             text=form.comment_text.data,
#             comment_author=current_user,
#             parent_post=requested_post
#         )
#         db.session.add(new_comment)
#         db.session.commit()
#
#     return render_template("post.html", post=requested_post, form=form, current_user=current_user)








if __name__ == "__main__":
    app.run(debug=True)