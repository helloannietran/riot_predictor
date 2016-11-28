from flask import Flask
from flask import render_template
from app import app
# from app.twitter.views import twitter

# app = Flask(__name__)
# app.register_blueprint(twitter, url_prefix='/twitter')


@app.route('/')
def home():
    return render_template('home.html',title='Home')

@app.route('/index')
def index():
    return render_template('index.html',title='Index')



if __name__ == '__main__':
    app.run()
