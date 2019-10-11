from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


# basic form example
class LoginForm(MyBaseForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 20)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")
    

class UploadForm(MyBaseForm):
    photo = FileField("Upload Image", validators=[FileRequired(),
                                                  FileAllowed(["jpg", "jpeg", "png", "gif"])])
    submit = SubmitField()

