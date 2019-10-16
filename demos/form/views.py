import os
import uuid
import warnings

from flask import (render_template, request, flash, redirect, url_for, current_app,
                   session, send_from_directory, after_this_request)
from loguru import logger

from forms import (LoginForm, UploadForm, MultiUploadForm, RichTextForm, NewPostForm,
                   SigninForm, RegisterForm, SigninForm2, RegisterForm2)
from utils import use_services, clear_form


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
    @after_this_request
    def remember_language(response):
        # 图片查看完就清掉
        if 'filenames' in session:
            session.pop('filenames')
        return response

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


def two_form():
    signin_form = SigninForm()
    register_form = RegisterForm()
    # 这2个form都会被选初始化(只要提交请求里面有与Form相同名称的字段)
    logger.info(f"SigninForm = {signin_form.data}")
    logger.info(f"RegisterForm = {register_form.data}")

    if signin_form.submit1.data and signin_form.validate():
        flash(f'SigninForm submit, username={signin_form.username.data}, password={signin_form.password.data}')
        return redirect(url_for("index"))
    elif register_form.submit2.data and register_form.validate():
        flash(f'RegisterForm submit, username={register_form.username.data}, email={register_form.email.data}')
        return redirect(url_for("index"))
    clear_form(signin_form, register_form)
    return render_template("2form.html", signin_form=signin_form, register_form=register_form)


# 只是用来显示form表单, 不用来提交
def multi_form_multi_view():
    signin_form = SigninForm2()
    register_form = RegisterForm2()
    return render_template("2form_2view.html", signin_form=signin_form, register_form=register_form)


def handle_sign():
    signin_form = SigninForm2()
    register_form = RegisterForm2()
    # 这2个form都会被选初始化(只要提交请求里面有与Form相同名称的字段)
    logger.info(f"SigninForm = {signin_form.data}")
    logger.info(f"RegisterForm = {register_form.data}")

    clear_form(register_form)
    if signin_form.validate_on_submit():
        flash(f'SigninForm submit, username={signin_form.username.data}, password={signin_form.password.data}')
        return redirect(url_for("index"))
    # 使用session传递报错信息
    session['errors'] = signin_form.errors
    return render_template("2form_2view_session.html", signin_form=signin_form, register_form=register_form)


def handle_register():
    signin_form = SigninForm2()
    register_form = RegisterForm2()
    # 这2个form都会被选初始化(只要提交请求里面有与Form相同名称的字段)
    logger.info(f"SigninForm = {signin_form.data}")
    logger.info(f"RegisterForm = {register_form.data}")

    clear_form(signin_form)
    if register_form.validate_on_submit():
        flash(f'RegisterForm submit, username={register_form.username.data}, email={register_form.email.data}')
        return redirect(url_for("index"))

    # 使用field.errors的提交传递报错信息
    return render_template("2form_2view.html", signin_form=signin_form, register_form=register_form)


# dropzone上传文件, 每上传一张图片就会用ajax发起一次请求
def dropzone_upload():
    if request.method == 'POST':  # dropzone通过ajax上传时, 会调用该方法
        if 'file' not in request.files:
            return 'This field is required.', 400  # 返回给dropzone的ajax请求的响应, 400的话dropzone会认为失败了
        f = request.files.get('file')
        if f and allowed_file(f.filename):
            filename = random_filename(f.filename)
            f.save(os.path.join(
                current_app.config['UPLOAD_PATH'], filename
            ))

            # https://stackoverflow.com/questions/48387783/behaviour-when-multiple-requests-modify-the-session-in-flask
            # flask的原生session是保存在客户端的, 当同一个客户几乎同时发起多张图片的上传请求时, 每次请求所带的session信息都是初始值,
            # 服务器端每次接收到的session['filenames']是互相独立的, 会被分别更新然后返回给客户端
            # 而客户端的cookie会被最后一次的返回值覆盖, 因此只要客户端的请求不是一个完成后再发起下一个, 就会存在竞态条件
            # 因此session是存在竞态条件, 解决方案是把数据存储在服务器端(并打上该客户的标识, 这个客户标识可以存在session中),
            # 总之对于需要频繁更新的值, 就不应该存在session中(至少是客户端session中), session应该只用来存储某个客户标识

            session.setdefault('filenames', []).append(filename)
            # 每次请求的filenames不同(容易理解: 该值来自不同的请求, 每次请求肯定不一样),
            # session是同一个对象(不同客户端的请求都是同一个对象, 但是不同客户端里面的值filenames不同哟)
            warnings.warn(f'filenames\'id={id(session.get("filenames"))}, session\'id={id(session)}')

            return 'Success', 200  # 返回给dropzone的ajax请求的响应, 200的话dropzone会认为成功了
        else:
            return 'Invalid file type.', 400
    return render_template('dropzone.html')


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
    {'rule': '/two-form', 'view_func': two_form, 'methods': ['GET', 'POST']},
    {'rule': '/multi-form-multi-view', 'view_func': multi_form_multi_view},
    {'rule': '/handle-signin', 'view_func': handle_sign, 'methods': ['POST']},
    {'rule': '/handle-register', 'view_func': handle_register, 'methods': ['POST']},
    {'rule': '/dropzone-upload', 'view_func': dropzone_upload, 'methods': ['GET', 'POST']},
]


def add_routes(app):
    for rule in rules:
        app.add_url_rule(**rule)
