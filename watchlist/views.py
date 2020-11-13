from flask import url_for, flash, render_template, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect

from watchlist import app, db
from watchlist.models import Movie, User


@app.route("/", methods=["GET", "POST"])
def index():
    """
    主页
    """
    # 如果用户添加了新的电影条目，即form的request请求变为了POST
    if request.method == "POST":
        # 如果用户为登陆，则不能添加电影条目，重定向
        if not current_user.is_authenticated:
            return redirect(url_for("index"))
        title = request.form.get("title")
        year = request.form.get("year")
        # 如果添加格式不对，重定向
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash("Invalid input.")
            return redirect(url_for("index"))
        # 向数据库添加电影条目
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash("Item created.")
        return redirect(url_for("index"))
    # 查询当前登陆用户，和所有电影条目，将查询结果传给主页并显示出来
    user = User.query.first()
    movies = Movie.query.all()
    return render_template("index.html", user=user, movies=movies)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    用户登陆
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("invalid input.")
            return redirect(url_for("login"))

        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash("Login success.")
            return redirect(url_for("index"))

        flash("Invalid username or password")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """
    用户登出
    """
    logout_user()
    flash("Goodbye.")
    return redirect(url_for("index"))


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """
    修改用户名
    """
    if request.method == "POST":
        username = request.form["username"]

        if not username or len(username) > 20:
            flash("Invalid input.")
            return redirect(url_for("settings"))

        current_user.username = username
        # current_user 会返回当前登录用户的数据库记录对象
        # #等同于下面的用法
        #  user = User.query.first()
        # user.name = name
        db.session.commit()
        flash("Settings updated.")
        return redirect(url_for("index"))

    return render_template("settings.html")


@app.route("/movie/edit/<int:movie_id>", methods=["GET", "POST"])
@login_required
def edit(movie_id):
    """
    编辑电影
    """
    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash("Invalid input")
            return redirect(url_for("edit", movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash("Item updated.")
        return redirect(url_for("index"))

    return render_template("edit.html", movie=movie)


@app.route("/movie/delete/<int:movie_id>", methods=["POST"])  # 只限接受POST请求
@login_required
def delete(movie_id):
    """
    删除对于电影的记录
    """
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item deleted.")
    return redirect(url_for("index"))
