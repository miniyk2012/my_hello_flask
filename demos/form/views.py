import os
import uuid

from flask import (render_template, request, flash, redirect, url_for, current_app,
                   session, send_from_directory)
from loguru import logger

from forms import LoginForm, UploadForm, MultiUploadForm, RichTextForm, NewPostForm
from utils import use_services


class Service1:
    @classmethod
    def work(cls):
        return "work1"


class Service2:
    @classmethod
    def work(cls):
        return "work2"


def index():
    return render_template('index.html')


def html():
    logger.info(current_app.root_path)
    if request.method == "POST":
        username = request.form.get('username')
        flash("Welcome, {}".format(username))
        return redirect(url_for("index"))
    return render_template('pure_html.html')


def do_work(s1, s2):
    return s1.work() + s2.work()


def basic():
    form = LoginForm()
    logger.info(form.data)
    if form.validate_on_submit():
        username = form.username.data
        flash(f"Welcome, {username}")
        return redirect(url_for("index"))
    return render_template("basic.html", form=form)


def bootstrap():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('bootstrap.html', form=form)


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(current_app.config["UPLOAD_PATH"], filename))
        flash("Upload success.")
        session["filenames"] = [filename]
        return redirect(url_for("upload", filenames=[filename]))
    return render_template("upload.html", form=form, filenames=request.args.getlist("filenames"), title="Upload Form")


def show_images():
    return render_template('uploaded.html')


# 这是一个图片读取接口
def get_file(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)


def allowed_file(filename):
    ext = os.path.splitext(filename)[1]
    return ext.split('.')[1] in current_app.config['ALLOWED_EXTENSIONS']


# 上传多张图片, 强烈怀念Restful API, 否则完全看不出需要哪些参数
def multi_upload():
    form = MultiUploadForm()
    if form.validate_on_submit():
        filenames = []
        if "photo" not in request.files:
            flash("服务器端验证: 需要上传图片哟")
            return redirect(url_for("multi_upload"))
        for file in request.files.getlist("photo"):
            if not file:
                flash("服务器端验证: 需要上传图片哟")
                return redirect(url_for("multi_upload"))
            if allowed_file(file.filename):
                filename = random_filename(file.filename)
                file.save(os.path.join(current_app.config["UPLOAD_PATH"], filename))
                filenames.append(filename)
            else:
                flash(f"不支持的文件类型: {file.filename}")
                session['filenames'] = filenames
                return redirect(url_for("multi_upload", filenames=filenames))
        flash("Upload success.")
        session['filenames'] = filenames
        return redirect(url_for("multi_upload", filenames=filenames))
    return render_template("upload.html", form=form, filenames=request.args.getlist("filenames"),
                           title="MultiUpload Form")

# 集成ckeditor
def integrate_ckeditor():
    form = RichTextForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        flash('Your post is published!')
        return render_template('post.html', title=title, body=body)
    return render_template('ckeditor.html', form=form)


# 2个提交按钮的判断
def submit2():
    form = NewPostForm()
    if form.validate_on_submit():
        if form.save.data:
            flash("save submit")
        elif form.publish.data:
            flash("publish submit")
        return redirect(url_for("index"))
    return render_template("submit2.html", form=form)


rules = [
    {'rule': '/', 'view_func': index, 'methods': ['GET', 'POST']},
    {'rule': '/html', 'view_func': html, 'methods': ['GET', 'POST']},
    {'rule': '/do-work', 'view_func': use_services(Service1, Service2)(do_work), 'methods': ['GET', 'POST'],
     "endpoint": "do_work"},
    {'rule': '/basic', 'view_func': basic, 'methods': ['GET', 'POST']},
    {'rule': '/bootstrap', 'view_func': bootstrap, 'methods': ['GET', 'POST']},
    {'rule': '/upload', 'view_func': upload, 'methods': ['GET', 'POST']},
    {'rule': '/uploaded-images', 'view_func': show_images},
    {'rule': '/uploads/<path:filename>', 'view_func': get_file},
    {'rule': '/multi-upload', 'view_func': multi_upload, 'methods': ['GET', 'POST']},
    {'rule': '/ckeditor', 'view_func': integrate_ckeditor, 'methods': ['GET', 'POST']},
    {'rule': '/submit2', 'view_func': submit2, 'methods': ['GET', 'POST']},

]


def add_routes(app):
    for rule in rules:
        app.add_url_rule(**rule)
