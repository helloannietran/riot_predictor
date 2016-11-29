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
from app.utils import violence_rating, get_cr_based_on_country


negative_words = []
positive_words = []

twitter = Blueprint('twitter', __name__,
                   template_folder='templates')

issue_list = [ ('1','Election'), ('2','Economy'), ('2','Jobs'), ('3','Food'), ('3','Water'), ('4','Environment Degradation'),
                ('5','Ethnic Discrimination'), ('6','Religion'), ('7','Education'), ('8','Foreign Affairs'), ('9','Domestic War'), 
                ('9','Violence'), ('10','Human Rights'), ('11','Sport')]



class MyForm(Form):
    search_tweet = StringField("Hastag")
    # city = StringField("City")
    country = StringField("Country")
    participants = StringField("# Participants")
    deaths = StringField("# Deaths")
    injuries = StringField("# Injuries")
    target = SelectField("Target", choices=[('something','something'),('works','works')])
    issue = SelectField("Issue", choices=issue_list)
    keyword = StringField("Search keyword")




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
    country = request.form['country']
    issue = int(request.form['issue'])

    v_rating = violence_rating(tweets)
    crime_rate = get_cr_based_on_country(country)
    target = int(request.form['target'])
    deaths = int(request.form['deaths'])
    npart = int(request.form['participants'])
    issue = int(request.form['issue'])
    
    values_list = [crime_rate,target,deaths,npart,v_rating,issue]
    riot_prob = str(calculate_riot_prob(values_list))
    return str(crime_rate)

def calculate_riot_prob(values_list):
    f = open(str(os.getcwd()) + '/app/predictor/rfmodel.pickle', 'rb')
    result = pickle.load(f)
    return result.predict(values_list)


