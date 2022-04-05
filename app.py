"""Flask app for Notes"""

from flask import Flask, render_template, redirect, request, flash, jsonify
from models import  db, connect_db, User
from forms import RegisterForm

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

    # Make sure you are using WTForms and that your password input hides the    characters that the user is typing!

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name."""

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

        return redirect("/secret")

    else:
        return render_template("register.html", form=form)

# GET /login
# Show a form that when submitted will login a user. This form should accept a username and a password.

# Make sure you are using WTForms and that your password input hides the characters that the user is typing!

# POST /login
# Process the login form, ensuring the user is authenticated and going to /secret if so.
# GET /secret
# Return the text “You made it!” (don’t worry, we’ll get rid of this soon)