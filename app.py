"""Flask app for Notes"""

from flask import Flask, render_template, redirect, request, flash, jsonify, session
from models import  db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, NewNoteForm, UpdateNoteForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.get('/')
def get_homepage():
    """Redirect to register"""

    return redirect("/register")

# =================== USER ROUTES ===================

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: Show a form that when submitted will register/create a user.
    This form should accept a username, password, email, first_name, and last_name."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password, email=email,
        first_name = first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username  # keep logged in
        flash("User added!")
        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # keep logged in
            flash("Logged in successfully!")
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Incorrect username/password"]

    return render_template("login.html", form=form)

@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)

    flash("Logged out successfully!")
    return redirect("/")

# ==================== USER ROUTES ====================

@app.get("/users/<username>")
def show_user(username):
    """ Show user's profile and their notes """

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    user = User.query.get_or_404(username)
    CSRFform = CSRFProtectForm()
    notes = user.notes

    return render_template("user.html", user=user, CSRFform=CSRFform, notes = notes)

@app.post("/users/<username>/delete")
def delete_user(username):
    """ Delete user from database """
    user = User.query.get_or_404(username)
 
    form = CSRFProtectForm()

    if form.validate_on_submit():

        Note.query.filter_by(owner=username).delete()
        session.pop("username", None)
        db.session.delete(user)
        db.session.commit()
        flash("You deleted a user successfully!")

        return redirect("/")


# ==================== NOTES ROUTES ====================

@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def add_note(username):
    """ Show form to add new note and handle new note."""

    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title,content=content,owner=username)

        db.session.add(note)
        db.session.commit()

        flash('New note added')
        return redirect(f"/users/{username}")

    return render_template("new_note.html", form=form)


@app.route('/notes/<int:note_id>/update', methods=["GET", "POST"])
def update_note(note_id):
    """ Show form to update new note and handle updated note."""

    note = Note.query.get_or_404(note_id)
    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data 
        note.content = form.content.data
        username = note.owner

        db.session.add(note)
        db.session.commit()

        flash('Note updated')
        return redirect(f"/users/{username}")

    return render_template("update_note.html", form=form)

@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """ Delete note from database """
    note = Note.query.get_or_404(note_id)
    username = note.owner
    form = CSRFProtectForm()

    if form.validate_on_submit():

        db.session.delete(note)
        db.session.commit()
        flash("Note was deleted!")

        return redirect(f"/users/{username}")