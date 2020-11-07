from flask import Flask
from flask import url_for
app = Flask(__name__)

@app.route('/')
def hello():
	return 'Welcome to My Watchlist!'

@app.route('/user/<name>')
def user_page(name):
	return 'User: %s' % name

@app.route('/test')
def test_url_for():
	print(url_for('hello'))
	print(url_for('user_page', name = '1'))
	print(url_for('user_page', name = '2'))
	print(url_for('test_url_for'))
	print(url_for('test_url_for', num=2))
	return 'Test page'

