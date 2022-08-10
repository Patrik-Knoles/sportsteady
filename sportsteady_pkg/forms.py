from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class JournalistForm(FlaskForm): 
   firstname = StringField("", validators=[DataRequired(message="First must be at least 5 characters long"),Length(min=5)])
   lastname = StringField("", validators=[DataRequired(message="Lastname must be at least 5 characters long"),Length(min=5)])
   email = StringField("", validators=[DataRequired(message="invalid email address"),Email()])
   address = TextAreaField()
   phone = StringField("", validators=[DataRequired(message="Invalid number format"), Length(min=14,max=14)])
   password = PasswordField("", validators=[DataRequired(),Length(min=7,max=10)])
   confirm_password = PasswordField("", validators=[DataRequired(message="Password Mismatch"),EqualTo("password")])
   submit = SubmitField()


class UserForm(FlaskForm): 
   firstname = StringField("", validators=[DataRequired(message="First must be at least 5 characters long"),Length(min=5)])
   lastname = StringField("", validators=[DataRequired(message="Lastname must be at least 5 characters long"),Length(min=5)])
   email = StringField("", validators=[DataRequired(message="invalid email address"),Email()])
   phone = StringField("", validators=[DataRequired(message="Invalid number format"), Length(min=14,max=14)])
   password = PasswordField("", validators=[DataRequired(),Length(min=3,max=10)])
   confirm_password = PasswordField("", validators=[DataRequired(message="Password Mismatch"),EqualTo("password")])
   submit = SubmitField()