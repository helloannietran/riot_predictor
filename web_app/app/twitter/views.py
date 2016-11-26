from flask import render_template,session
from flask import Blueprint
from flask import request, send_file    
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, widgets, HiddenField
from wtforms.fields.html5 import DateField
from sqlalchemy import create_engine
from twython import Twython


twitter = Blueprint('twitter', __name__,
                   template_folder='templates')


class MyForm(Form):
    search_tweet = StringField("Hastag")


@twitter.route('/')
def home():
    form = MyForm()
    return render_template('search_twitter.html', form = form)


@twitter.route('/submit', methods=('GET', 'POST'))
def submit():
    query = request.form['search_tweet']
    oauth_token = "802218282954747905-aibLqJnV93MWB8ZFEvhpQa5HTjNaNVX"
    oauth_token_secret = "lWnLP0MiJrNanfILvX48SerOXiiUYr9zo8UxnochCcqJz"
    app_key = "pLeOpV3TP1l3SGyNFjGfPUdgM"
    app_secret = "xoGYtBc2SujcWnWEDxNYd07Zv1MCTW57aBQVhwK90d0FhaqWIH"


    twitter = Twython(app_key=app_key, 
                app_secret=app_secret, 
                oauth_token=oauth_token, 
                oauth_token_secret=oauth_token_secret)

    search = twitter.search(q=query,count=100)

    tweets = [ tweet['text'] for tweet in search['statuses']]
    return(str(tweets))
    # return tweets
    # for tweet in tweets:
    #   # print(tweet['id_str'])
    #   print(tweet['text'])