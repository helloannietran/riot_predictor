from flask import Flask
from app.twitter.views import twitter


app = Flask(__name__)
app.register_blueprint(twitter, url_prefix='/twitter')


app.config.from_pyfile('config.py')

from app import views