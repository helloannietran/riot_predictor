from flask import render_template,session
from flask import Blueprint
from flask import request, send_file    
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, widgets, HiddenField
from wtforms.fields.html5 import DateField
from sqlalchemy import create_engine
from twython import Twython
import os
import re
import pickle
from app.utils import get_cr_based_on_country, violence_rating
from article_handler import save_articles


articles = Blueprint('articles', __name__,
                   template_folder='templates')

issue_list = [ ('1','Election'), ('2','Economy'), ('2','Jobs'), ('3','Food'), ('3','Water'), ('4','Environment Degradation'),
                ('5','Ethnic Discrimination'), ('6','Religion'), ('7','Education'), ('8','Foreign Affairs'), ('9','Domestic War'), 
                ('9','Violence'), ('10','Human Rights'), ('11','Sport')]


class MyForm(Form):
    # crime_rate = StringField("Crime Rate")
    city = StringField("City")
    country = StringField("Country")
    participants = StringField("# Participants")
    deaths = StringField("# Deaths")
    injuries = StringField("# Injuries")
    target = SelectField("Target", choices=[('something','something'),('works','works')])
    issue = SelectField("Issue", choices=issue_list)


@articles.route('/')
def home():
    form = MyForm()
    return render_template('search_articles.html', form = form)


@articles.route('/submit', methods=('GET', 'POST'))
def submit():
    country = request.form['country']
<<<<<<< Updated upstream
    issue = int(request.form['issue'])
    print(issue)
=======
    articles = save_articles(request.form['keyword'])
    v_rating = violence_rating(articles)
    riot_prob = str(calculate_riot_prob(v_rating))

    crime_rate = request.form['search_tweet']
    target = request.form['search_tweet']
    deaths = request.form['search_tweet']
    npart = request.form['search_tweet']
    issue = request.form['search_tweet']
    [crime_rate,target,deaths,npart,violence_rating,issue]
>>>>>>> Stashed changes
    crime_rate = get_cr_based_on_country(country)
    return(str(crime_rate))





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


