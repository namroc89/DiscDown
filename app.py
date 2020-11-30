from flask import Flask, request, render_template, redirect, flash, session, g
from models import db, connect_db, GroupRound, User, UserRound, Follows
import requests
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from flask_debugtoolbar import DebugToolbarExtension
from forms import LoginForm, RegisterForm, EditUser, NewRound
from psycopg2.errors import UniqueViolation
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


def user_logout():
    """Log out user"""
    if ACTIVE_USER in session:
        del session[ACTIVE_USER]


def get_course_by_id(course_id):
    """A call to the API to gather course information based on the course id
    returns a single JSON course response"""
    res = requests.get(f"{API_URL}", params={
                       'key': API_KEY, 'mode': 'crseinfo', 'id': course_id, 'sig': ID_SEARCH_SIG})
    if not res:
        return []

    return res.json()


def get_course_by_name(name):
    """search the API for courses by name. Returns list of JSON objects"""
    res = requests.get(f"{API_URL}", params={
                       'key': API_KEY, 'mode': 'findname', 'name': name, 'sig': NAME_SEARCH_SIG})
    if not res:
        return []
    return res.json()


def get_hole_info(course_id):
    """search hole information for selected course. Returns json list of holes and information"""
    res = requests.get(f"{API_URL}", params={
        'key': API_KEY, 'mode': "holeinfo", 'id': course_id, 'sig': HOLE_INFO_SIG
    })
    if not res:
        return []
    return res.json()


def get_course_photo(course_id):
    """retreive a course photo from the API. Returns URL"""
    res = requests.get(f"{API_URL}", params={
        'key': API_KEY, 'mode': "crsephto", 'id': course_id, 'sig': PHOTO_SEARCH_SIG
    })
    if not res:
        return None
    return res.json()['course_photo_url_medium']


def search_by_zip(zip):
    """Searches API for course close to zip. Returns list of JSON objects"""
    res = requests.get(f"{API_URL}", params={
        'key': API_KEY, 'mode': "findzip", 'zip': zip, 'sig': ZIP_SEARCH_SIG
    })
    if not res:
        return []
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

        except:
            flash("Username or Email is already being used", "danger")
            return render_template("register.html", form=form)

        user_login(new_user)
        return redirect('/home')
    else:
        return render_template("register.html", form=form)


@app.route('/logout', methods=['POST'])
def logout_user():
    if not g.user:
        flash("Log in before you can log out!", "warning")
        return redirect('/')
    user_logout()
    flash("Log out was successful!", 'success')
    return redirect('/')


@app.route('/home')
def home_page():
    """landing page when the site is visited"""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')
    rounds = UserRound.query.order_by(UserRound.date.desc()).all()

    return render_template('userhome.html', rounds=rounds)

#######################################
# Course Routes #


@app.route('/course_details/<int:id>')
def show_course_details(id):
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')
    rounds = UserRound.query.filter(
        UserRound.course_id == id).order_by(UserRound.date.desc()).all()
    try:
        course = get_course_by_id(id)

    except:
        flash("An error occured, try again", "danger")
        return redirect('/')
    return render_template('/course/course_rounds.html', course=course, rounds=rounds)

####################################
# User Routes #


@app.route('/users/<int:id>')
def show_user_details(id):
    """shows a users details to another logged in user. If page is logged in users details, can be edited."""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')
    user = User.query.get_or_404(id)
    following = [f.id for f in user.following] + [user.id]
    following_rounds = (UserRound.query.filter(UserRound.user_id.in_(following))
                        .order_by(UserRound.date.desc())
                        .all())
    return render_template('/user/user_details.html', user=user, following_rounds=following_rounds)


@app.route('/users/<int:id>/rounds')
def show_user_rounds(id):
    """Show user page with most recent rounds"""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')
    user = User.query.get_or_404(id)
    return render_template('/user/user_rounds.html', user=user)


@app.route('/users/<int:id>/following')
def show_user_follows(id):
    """Show user page with all followed users"""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')
    user = User.query.get_or_404(id)
    return render_template('/user/following.html', user=user)


@app.route('/users/<int:id>/followers')
def show_user_followers(id):
    """Show user page with all followers"""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')
    user = User.query.get_or_404(id)
    return render_template('/user/followers.html', user=user)


@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    """Shows edit user page and submits changes to the DB"""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')
    if g.user.id != id:
        flash("Unautherized to edit user", 'danger')
        return redirect('/')
    user = g.user
    form = EditUser(obj=user)
    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            try:
                user.username = form.username.data
                user.first_name = form.first_name.data
                user.last_name = form.last_name.data
                user.email = form.email.data
                user.location = form.location.data
                user.bio = form.bio.data
                user.fav_course = form.fav_course.data
                user.avatar = form.avatar.data
                db.session.commit()

            except (IntegrityError, InvalidRequestError, UniqueViolation):
                db.session.rollback()
                flash("Username or Email is already being used", "danger")
                return render_template('user/edit_user.html', user=user, form=form)
            flash("Profile edited successfully!", 'success')
            return redirect(f"/users/{user.id}")
        flash("Incorrect Password", 'danger')
        return render_template('user/edit_user.html', user=user, form=form)
    else:
        return render_template('user/edit_user.html', user=user, form=form)


@app.route('/users/<int:id>/new_round', methods=['GET', 'POST'])
def add_new_round(id):
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')
    if g.user.id != id:
        flash("Unautherized to add round for that user", 'danger')
        return redirect('/')
    form = NewRound()
    user = g.user

    if form.validate_on_submit():
        course = get_course_by_name(form.course_name.data)
        course = course[0]
        if not course:
            flash("No courses found with that name", "warning")
            return render_template('user/new_round.html', form=form, user=user)
        course_name = course["name"]
        course_id = course["course_id"]
        date = form.date.data
        score = form.score.data
        notes = form.notes.data
        user_id = user.id

        new_round = UserRound(user_id=user_id, course_id=course_id,
                              course_name=course_name, date=date, score=score, notes=notes)
        db.session.add(new_round)
        try:
            db.session.commit()
        except:
            flash('Something went wrong, try again', 'danger')
            return render_template('user/new_round.html', form=form)
        flash('Round added successfully', 'success')
        return redirect(f'/users/{id}')
    else:
        return render_template('user/new_round.html', form=form, user=user)


@app.route("/users/<int:id>/follow", methods=['POST'])
def follow_user(id):
    """Adding user to followed users"""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')
    if g.user.id == id:
        flash("Following yourself is a little vain, don't you think?", "warning")
        return redirect('/')

    followed_user = User.query.get_or_404(id)
    followed_user.followers.append(g.user)
    db.session.commit()

    return redirect(f"/users/{id}")


@app.route("/users/<int:id>/unfollow", methods=['POST'])
def unfollow_user(id):
    """removes user form followed user"""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')
    if g.user.id == id:
        flash("Can't unfollow yourself, unfortunately", "warning")
        return redirect('/')

    followed_user = User.query.get_or_404(id)
    followed_user.followers.remove(g.user)
    db.session.commit()

    return redirect(f"/users/{id}")


###################################
# Search Routes #


@app.route('/course_search_name')
def search_course_by_name_results():
    """Shows results of a search for courses by name."""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')

    search = request.args['course-name-input']
    courses = get_course_by_name(search)
    return render_template('/search/course_search_results.html', courses=courses)


@app.route('/course_search_zip')
def search_course_by_zip_results():
    """Shows results of a search for courses by zipcode."""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')

    search = request.args['course-zip']
    courses = search_by_zip(search)
    return render_template('/search/course_search_results.html', courses=courses)


@app.route('/user_search')
def user_search_results():
    """Shows results of a search for users by username."""
    if not g.user:
        flash("Please Log in or Register!", "danger")
        return redirect('/')

    search = request.args['user-username-input']
    users = User.query.filter(User.username.like(f"%{search}%")).all()
    return render_template('/search/user_search_results.html', users=users)

########################################################


########################################################################
# API calls from the front end #
