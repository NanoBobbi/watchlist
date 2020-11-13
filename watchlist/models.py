from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db


# 用于存储用户的 User 模型类
class User(db.Model, UserMixin):
    """
    User继承自UserMixin，其中最常用的是 is_authenticated 属性：
    如果当前用户已经登录，那么 current_user.is_authenticated 会返回 True，否则返回 False
    有了current_user 变量和这几个验证方法和属性，我们可以很轻松的判断当前用户的认证状态。
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 用于存储电影的 Movie 模型类
class Movie(db.Model):
    """
    id为主键
    title为电影名称
    year为电影上映日期
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
