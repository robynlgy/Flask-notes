from click import password_option
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    """Form for registering new user."""

    username = StringField("Username: ",
                validators = [InputRequired(),
                Length(1,20,"Invalid username")])
    password = PasswordField("Password: ",
                validators = [InputRequired(),
                Length(1,100,"Invalid password")])
    email = StringField("Email: ",
                validators = [InputRequired(),
                Length(1,50,"Invalid email")])
    first_name = StringField("First Name: ",
                    validators = [InputRequired(),
                    Length(1,30,"Invalid first name")])
    last_name = StringField("Last Name: ",
                    validators = [InputRequired(),
                    Length(1,30,"Invalid last name")])


class LoginForm(FlaskForm):
    """Form for login user."""

    username = StringField("Username: ",
                validators = [InputRequired(), Length(1,20,"Invalid username")])
    password = PasswordField("Password: ",
                validators = [InputRequired(), Length(1,100,"Invalid password")])


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""

class NoteForm(FlaskForm):
    """Form for creating a new note or updating it."""

    title = StringField("Note Title: ",
                validators = [InputRequired(),
                Length(1,100,"Invalid title")])
    content = TextAreaField("Content: ",
                validators = [InputRequired()])


