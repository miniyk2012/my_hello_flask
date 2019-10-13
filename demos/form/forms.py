from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (BooleanField, StringField, PasswordField,
                     SubmitField, MultipleFileField, TextAreaField
                     )
from wtforms.validators import DataRequired, Length, Email


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
    photo = FileField("Upload Image", validators=[FileRequired("请上传图片"),
                                                  FileAllowed(["jpg", "jpeg", "png", "gif"])])
    submit = SubmitField()


class MultiUploadForm(MyBaseForm):
    # 注: photo=MultipleFileField是WTF原生字段, 因此不支持flask的FileAllowed功能
    photo = MultipleFileField("Upload Images", validators=[DataRequired(message="请上传图片们")])
    submit = SubmitField()


# Ckeditor
class RichTextForm(MyBaseForm):
    title = StringField("Title", validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField("Body", validators=[DataRequired()])
    submit = SubmitField("Publish")


# multiple submit button
class NewPostForm(MyBaseForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('Save')
    publish = SubmitField('Publish')


class SigninForm(MyBaseForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    submit1 = SubmitField()


class RegisterForm(MyBaseForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 50)])
    email = StringField('Email', validators=[DataRequired(), Email(message="邮箱格式错误"), Length(5, 100)])
    submit2 = SubmitField()


class SigninForm2(MyBaseForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    submit = SubmitField()


class RegisterForm2(MyBaseForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 50)])
    email = StringField('Email', validators=[DataRequired(), Email(message="邮箱格式错误"), Length(5, 100)])
    submit = SubmitField()
