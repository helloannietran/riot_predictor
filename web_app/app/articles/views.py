from flask import render_template,session
from flask import Blueprint
from flask import request, send_file    
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, widgets, HiddenField
from wtforms.fields.html5 import DateField
from sqlalchemy import create_engine
from twython import Twython
from os.path import join
import re
import pickle


articles = Blueprint('articles', __name__,
                   template_folder='templates')


class MyForm(Form):
    crime_rate = StringField("Crime Rate")
    city = StringField("City")
    country = StringField("Country")
    participants = StringField("# Participants")
    deaths = StringField("# Deaths")
    injuries = StringField("# Injuries")
    target = SelectField("Target", choices=[('something','something'),('works','works')])
    issue = SelectField("Issue", choices=[('something','something'),('works','works')])


@articles.route('/')
def home():
    form = MyForm()
    return render_template('search_articles.html', form = form)


@articles.route('/submit', methods=('GET', 'POST'))
def submit():
    return ("This works!!")

