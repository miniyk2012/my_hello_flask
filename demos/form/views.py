from flask import render_template, request, flash, redirect, url_for


def index():
    return render_template('index.html')


def html():
    if request.method == "POST":
        username = request.form.get('username')
        flash("Welcome, {}".format(username))
        return redirect(url_for("index"))
    return render_template('pure_html.html')


rules = [
    {'rule': '/', 'view_func': index, 'methods': ['GET', 'POST']},
    {'rule': '/html', 'view_func': html, 'methods': ['GET', 'POST']},
]


def add_routes(app):
    for rule in rules:
        app.add_url_rule(**rule)
