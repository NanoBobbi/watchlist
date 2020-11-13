from flask import render_template
from watchlist import app


@app.errorhandler(404)
def page_not_found(e):
    """
    传入要处理的错误代码
    """
    return render_template('errors/404.html'), 404
