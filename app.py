from flask import Flask
from flask import url_for, render_template, request,redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_manager, UserMixin, login_user, logout_user,login_required, current_user, LoginManager
import os
import sys
import  click


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'dev'

class User(db.Model, UserMixin):
    """
    docstring
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    """
    docstring
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    """
    Initialize the database.
    """
    if drop:
        db.drop_all()
        click.echo('Dropped database.')
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login')
def admin(username, password):
    """
    Create user.
    """
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user ...')
        # user.username = username
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user ...')
        user = User(username=username, name='admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@app.route("/",methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    user = User.query.first()
    movies = Movie.query.all()
    return render_template("index.html", user=user, movies=movies)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        username = request.form['username']

        if not username or len(username) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.username = username
        # current_user 会返回当前登录用户的数据库记录对象
        # #等同于下面的用法
        #  user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/movie/edit/<int:movie_id>', methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])#只限接受POST请求
@login_required
def delete(movie_id):
    """
    删除对于电影的记录
    """
    movie = Movie.query.get_or_404(moive_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

# @app.route("/test")
# def test_url_for():
#     print(url_for("index"))
#     print(url_for("user_page", name="1"))
#     print(url_for("user_page", name="2"))
#     print(url_for("test_url_for"))
#     print(url_for("test_url_for", num=2))
#     return "Test page"

@app.cli.command()
def forge():
    """
    Generate fake data.
    """
    db.create_all()

    name = "Grey Li"
    movies = [
        {"title": "My Neighbor Totoro", "year": "1988"},
        {"title": "Dead Poets Society", "year": "1989"},
        {"title": "A Perfect World", "year": "1993"},
        {"title": "Leon", "year": "1994"},
        {"title": "Mahjong", "year": "1996"},
        {"title": "Swallowtail Butterfly", "year": "1996"},
        {"title": "King of Comedy", "year": "1999"},
        {"title": "Devils on the Doorstep", "year": "1999"},
        {"title": "WALL-E", "year": "2008"},
        {"title": "The Pork of Music", "year": "2012"},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.errorhandler(404)
def page_not_found(e):
    """
    传入要处理的错误代码
    """
    user = User.query.first()
    return render_template('404.html'), 404

@app.context_processor
# 这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文 环境中，因此可以直接在模板中使用。
def inject_user():
    # 函数名可以随意修改
    user = User.query.first()
    return dict(user = user)

