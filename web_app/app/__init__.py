from flask import Flask
from app.twitter.views import twitter
from app.articles.views import articles


app = Flask(__name__)
app.register_blueprint(twitter, url_prefix='/twitter')
app.register_blueprint(articles, url_prefix='/articles')

app.config.from_pyfile('config.py')

from app import views