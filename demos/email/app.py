import os
from threading import Thread
import sendgrid
from flask import Flask, request, flash, render_template, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from sendgrid.helpers.mail import Mail as SGMail
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'secret string'))


def config_netease_mail():
    app.config.update(
        MAIL_SERVER=os.getenv('MAIL_SERVER'),
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USE_TLS=False,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=('Thomas Young', os.getenv('MAIL_USERNAME'))
    )
    global mail
    mail = Mail(app)
    return mail


def config_sendgrid_mail():
    app.config.update(
        MAIL_SERVER='smtp.sendgrid.net',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('SENDGRID_API_KEY'),
        MAIL_DEFAULT_SENDER=('Thomas Young', os.getenv('MAIL_USERNAME'))
    )
    global mail
    mail = Mail(app)
    return mail


# send over SMTP
def send_smtp_mail(subject, to, body):
    """from app import send_smtp_mail
    send_smtp_mail('hello', '812350401@qq.com', '你好呀')
    """
    mail = config_netease_mail()
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
    # mail = config_sendgrid_mail()
    # message = Message(subject, recipients=[to], body=body)
    # mail.send(message)
    send_by_api(body, subject, to)


def send_by_api(body, subject, to):
    sg = sendgrid.SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    from_email = 'ThomasYoung <yk_ecust_2007@163.com>'
    text_content = body
    html_content = '<h1>订阅</h1>'
    print(body, subject, to)
    email = SGMail(from_email=from_email, subject=subject, to_emails=to, plain_text_content=text_content,
                   html_content=html_content)
    response = sg.send(email)

    print('code', response.status_code)
    print('body', response.body)
    print('headers', response.headers)


# send email asynchronously
def _send_async_mail(app, subject, to, body):
    with app.app_context():
        mail = config_netease_mail()
        config_netease_mail()
        message = Message(subject, recipients=[to], body=body)  # 我发现这一步特别慢, 因此也搬到另一个线程里面来
        mail.send(message)


def send_async_mail(subject, to, body):
    thr = Thread(target=_send_async_mail, args=[app, subject, to, body])
    thr.start()
    return thr


# send email with HTML body
def send_subscribe_mail(subject, to, **kwargs):
    mail = config_netease_mail()
    message = Message(subject, recipients=[to], sender='Flask Weekly <%s>' % os.getenv('MAIL_USERNAME'))
    message.body = render_template('emails/subscribe.txt', **kwargs)
    message.html = render_template('emails/subscribe.html', **kwargs)
    mail.send(message)


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
        elif form.submit_api.data:  # True or False
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


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        send_subscribe_mail('Subscribe Success!', email, name=name)
        flash('Confirmation email have been sent! Check your inbox.')
        return redirect(url_for('subscribe'))
    return render_template('subscribe.html', form=form)


@app.route('/unsubscribe')
def unsubscribe():
    flash('Want to unsubscribe? No way...')
    return redirect(url_for('subscribe'))
