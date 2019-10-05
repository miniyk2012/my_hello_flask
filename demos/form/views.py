from flask import render_template


def index():
    return render_template('index.html')


def html():
    return render_template('pure_html.html')


rules = [
    {'rule': '/', 'view_func': index, 'methods': ['GET', 'POST']},
    {'rule': '/html', 'view_func': html, 'methods': ['GET', 'POST']},
]


def add_routes(app):
    for rule in rules:
        app.add_url_rule(**rule)
