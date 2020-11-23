from flask import Flask, request, render_template, redirect, flash, session, g
from models import db, connect_db, GroupRound, User, UserRound, Follows
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm, RegisterForm
from secret import API_KEY, NAME_SEARCH_SIG, ZIP_SEARCH_SIG, LOC_SEARCH_SIG, ID_SEARCH_SIG, PHOTO_SEARCH_SIG, HOLE_INFO_SIG

app = Flask(__name__)

ACTIVE_USER = "active_user_id"

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


@app.route('/')
def base():
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
        return redirect('/home.html')
    else:
        return render_template("register.html", form=form)
