from flask import render_template,session
from flask import Blueprint
from flask import request, send_file    
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, widgets, HiddenField
from wtforms.fields.html5 import DateField
from sqlalchemy import create_engine
from twython import Twython
#from parse_file import get_all_files_in_dir
from os.path import join
import re
import pickle

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
    #return(str(tweets))
    ##Changed here
    return (violence_rating(str(tweets)))
    ##Chenge ended here
    # return tweets
    # for tweet in tweets:
    #   # print(tweet['id_str'])
    #   print(tweet['text'])

def violence_rating(tweets):
    negs=0
    poses=0
    total=0
    with open("negative_words.txt") as negative_file:
        for l in negative_file:
            negative_words.append(l.strip())

    with open("positive_words.txt") as positive_file:
        for l in positive_file:
            positive_words.append(l.strip())

    negative_count, total_count = count_words(tweets, negative_words)
    positive_count, total_count = count_words(tweets, positive_words)
    negs += negative_count
    poses += positive_count
    total += total_count
    out_val = (poses - negs)*100.0/total if total > 0 else 'None'
    return str(calculate_riot_prob(out_val))

def count_words(text, ref_words):
    all_words = text.split()
    regex = re.compile('[^a-zA-Z]')
    all_words = [regex.sub('',  w).strip() for w in all_words if len(w)<20]
    
    count = 0
    for word in all_words:
        # print word
        if word.strip().lower() in ref_words:
            # print word
            count += 1
    total_count = len(all_words)
    return count, total_count

def calculate_riot_prob(out_val):
    f = open('/Users/sathani/Desktop/riot/web_app/app/twitter/my_classifier.pickle', 'rb')
    result = pickle.load(f)
    f.close()
    crime_rate = 2.34
    target = 4
    duration = 40
    deaths = 40
    npart = 100
    violence_rating = out_val
    issue = 3
    return result.predict([crime_rate,target,duration,deaths,npart,violence_rating,issue])


