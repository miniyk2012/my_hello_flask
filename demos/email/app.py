import os

from flask import Flask, request, flash, render_template, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'secret string'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=('Thomas Young', os.getenv('MAIL_USERNAME'))
)
mail = Mail(app)


# send over SMTP
def send_smtp_mail(subject, to, body):
    """from app import send_smtp_mail
    send_smtp_mail('hello', '812350401@qq.com', '你好呀')
    """
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)


class SubscribeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')


class EmailForm(FlaskForm):
    to = StringField('To', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit_smtp = SubmitField('Send with SMTP')
    submit_api = SubmitField('Send with SendGrid API')
    submit_async = SubmitField('Send with SMTP asynchronously')


def send_api_mail(subject, to, body):
    pass


def send_async_mail(subject, to, body):
    pass


@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if form.validate_on_submit():
        to = form.to.data
        subject = form.subject.data
        body = form.body.data
        if form.submit_smtp.data:
            send_smtp_mail(subject, to, body)
            method = request.form.get('submit_smtp')
        elif form.submit_api.data:
            send_api_mail(subject, to, body)
            method = request.form.get('submit_api')
        else:
            send_async_mail(subject, to, body)
            method = request.form.get('submit_async')

        flash('Email sent %s! Check your inbox.' % ' '.join(method.split()[1:]))
        return redirect(url_for('index'))
    form.subject.data = 'Hello, World!'
    form.body.data = 'Across the Great Wall we can reach every corner in the world.'
    return render_template('index.html', form=form)
