import os

from flask import Flask, render_template, Markup, flash, redirect, url_for
from loguru import logger

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

user = {
    'username': 'Thomas Young',
    'bio': 'A man who love math and freedom.',
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/watchlist')
def watchlist():
    markup_text = Markup('<h3>Hello, Flask!<h3>')
    return render_template('watchlist.html', user=user, movies=movies, p_value='<p>content</p>',
                           markup_text=markup_text)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/watchlist2')
def watchlist_with_static():
    return render_template('watchlist_with_static.html', user=user, movies=movies)


# message flashing
@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    flash('我是杨恺')
    return redirect(url_for('index'))


# register template context handler
@app.context_processor
def inject_foo():
    foo = "this is foo"
    return {"foo": foo, 'alert_color': 'purple'}  # alert_color用于传给css的自定义变量--alert-color, 设置flash的颜色


# 向模板注入函数1
@app.context_processor
def inject_fibonacci():
    logger.info('invoke inject_fabonaci')

    def fibonacci(n):
        a, b = 1, 1
        i = 1
        while i <= n:
            a, b = b, a + b
            i += 1
        return a

    return dict(fibonacci=fibonacci)


# 向模板注入函数2
@app.template_global()
def bar():
    logger.info('invoke bar')
    return 'I am a bar'


# register template filter
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')


def laugh(s, n=1):
    return s + ' ,ha' * n + '!'


# register template filter
app.add_template_filter(laugh)


# register template test
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
