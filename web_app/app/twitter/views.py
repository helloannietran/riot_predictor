from flask import render_template,session
from flask import Blueprint
from flask import request, send_file    
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, widgets, HiddenField
from wtforms.fields.html5 import DateField
from sqlalchemy import create_engine
from twython import Twython
import os
#from parse_file import get_all_files_in_dir
from os.path import join
import re
import pickle
from app.utils import violence_rating


negative_words = []
positive_words = []

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
    if(query == ""):
        return("no keyword")
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
    # return(str(tweets))
    ##Changed here
    v_rating = violence_rating(str(tweets))
    riot_prob = str(calculate_riot_prob(v_rating))

    crime_rate = request.form['search_tweet']
    target = request.form['search_tweet']
    deaths = request.form['search_tweet']
    npart = request.form['search_tweet']
    issue = request.form['search_tweet']
    [crime_rate,target,deaths,npart,violence_rating,issue]
    # str(calculate_riot_prob(violence_rating(str(tweets)))
    return riot_prob
    ##Chenge ended here
    # return tweets
    # for tweet in tweets:
    #   # print(tweet['id_str'])
    #   print(tweet['text'])

def calculate_riot_prob(values_list):
    # print(os.getcwd())
    f = open(str(os.getcwd()) + '/app/predictor/rfmodel.pickle', 'rb')
    # result = pickle.load(f)
    # f.close()
    # crime_rate = 2.34
    # target = 4
    # duration = 40
    # deaths = 40
    # npart = 100
    # violence_rating = out_val
    # issue = 3
    return 1
    # return result.predict([crime_rate,target,deaths,npart,violence_rating,issue])


