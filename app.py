from flask import Flask, request, render_template, redirect, flash, session, g
from models import db, connect_db, GroupRound, User, UserRound, Follows
import requests
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm, RegisterForm
from secret.secret import API_KEY, NAME_SEARCH_SIG, ZIP_SEARCH_SIG, LOC_SEARCH_SIG, ID_SEARCH_SIG, PHOTO_SEARCH_SIG, HOLE_INFO_SIG

app = Flask(__name__)

ACTIVE_USER = "active_user_id"

API_URL = "https://www.dgcoursereview.com/api_test/"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///discgolf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "hellomybaby12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if ACTIVE_USER in session:
        g.user = User.query.get(session[ACTIVE_USER])

    else:
        g.user = None


def user_login(user):
    """Log in user"""
    session[ACTIVE_USER] = user.id


def user_logout(user):
    """Log out user"""
    if ACTIVE_USER in session:
        del session[ACTIVE_USER]


def get_course_by_id(course_id):
    """A call to the API to gather course information based on the course id
    returns a single JSON course response"""
    res = requests.get(f"{API_URL}", params={
                       'key': API_KEY, 'mode': 'crseinfo', 'id': course_id, 'sig': ID_SEARCH_SIG})
    return res.json()


def get_course_by_name(name):
    """search the API for courses by name. Returns list of JSON objects"""
    res = requests.get(f"{API_URL}", params={
                       'key': API_KEY, 'mode': 'findname', 'name': name, 'sig': NAME_SEARCH_SIG})
    return res.json()


def get_hole_info(course_id):
    """search hole information for selected course. Returns json list of holes and information"""
    res = requests.get(f"{API_URL}", params={
        'key': API_KEY, 'mode': "holeinfo", 'id': course_id, 'sig': HOLE_INFO_SIG
    })
    return res.json()


def get_course_photo(course_id):
    """retreive a course photo from the API. Returns URL"""
    res = requests.get(f"{API_URL}", params={
        'key': API_KEY, 'mode': "crsephto", 'id': course_id, 'sig': PHOTO_SEARCH_SIG
    })

    return res.json()['course_photo_url_medium']


def search_by_zip(zip):
    """Searches API for course close to zip. Returns list of JSON objects"""
    res = requests.get(f"{API_URL}", params={
        'key': API_KEY, 'mode': "findzip", 'zip': zip, 'sig': ZIP_SEARCH_SIG
    })

    return res.json()


@app.route('/')
def base():
    if g.user:
        return redirect('/home')
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handles User Login"""

    form = LoginForm()
    if g.user:
        flash("Already logged in, log out to log in as different user", "warning")
        return redirect('/')
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            user_login(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect("/")

        flash("Invalid login information", "danger")

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """page with form to register a new user"""
    form = RegisterForm()
    if g.user:
        flash("Already logged in, log out to register new user", "warning")
        return redirect('/')

    if form.validate_on_submit():
        try:
            new_user = User.signup(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username or Email is already being used", "danger")
            return render_template("register.html", form=form)

        user_login(new_user)
        return redirect('/home')
    else:
        return render_template("register.html", form=form)


@app.route('/home')
def home_page():
    """landing page when the site is visited"""
    if not g.user:
        return redirect('/')

    return render_template('userhome.html')
