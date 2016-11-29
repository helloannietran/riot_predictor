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

issue_list = [('1','Election'), ('2','Economy'), ('2','Jobs'), ('3','Food'), ('3','Water'), ('4','Environment Degradation'),
                ('5','Ethnic Discrimination'), ('6','Religion'), ('7','Education'), ('8','Foreign Affairs'), ('9','Domestic War'), 
                ('9','Violence'), ('10','Human Rights'), ('11', 'Pro-government'), ('12', 'Economic Resources'), ('12', 'Assets'),
                ('13','Sport')]

target_list = [('1', 'Opposition Supporters (Citizens)'), ('2', 'Government'), ('3', 'Police'), ('4', 'Corporations/Companies'), 
                ('5', 'Religious Group'), ('6', 'Fans'), ('7', 'Military'), ('8', 'Tourist')]

participants_list = [('1', 'less than 10'), ('2', '10 - 100'), ('3', '101 - 1000'), ('4', '1001 - 10,000'), ('5', '10,001 - 100,000'), 
                        ('6', '100,001 - 1,000,000'), ('7', 'over 1,000,000')]

country_list = [('Canada', 'Canada'), ('Saudi-Arabia', 'Saudi-Arabia'), ('Ethiopia', 'Ethiopia'), ('Swaziland', 'Swaziland'), 
                ('Palestine', 'Palestine'), ('Argentina', 'Argentina'), ('Bolivia', 'Bolivia'), ('Cameroon', 'Cameroon'), 
                ('Bahrain', 'Bahrain'), ('Guatemala', 'Guatemala'), ('Spain', 'Spain'), ('Liberia', 'Liberia'), 
                ('Netherlands', 'Netherlands'), ('Pakistan', 'Pakistan'), ('Tanzania', 'Tanzania'), ('Gabon', 'Gabon'), 
                ('Yemen', 'Yemen'), ('Jamaica', 'Jamaica'), ('South-Africa', 'South-Africa'), ('Albania', 'Albania'), 
                ('El-Salvador', 'El-Salvador'), ('India', 'India'), ('Lesotho', 'Lesotho'), ('United-States', 'United-States'), 
                ('Kenya', 'Kenya'), ('Turkey', 'Turkey'), ('Afghanistan', 'Afghanistan'), ('South-Sudan', 'South-Sudan'), 
                ('Bangladesh', 'Bangladesh'), ('Eritrea', 'Eritrea'), ('Hungary', 'Hungary'), ('Mongolia', 'Mongolia'), 
                ('France', 'France'), ('Rwanda', 'Rwanda'), ('Somalia', 'Somalia'), ('Peru', 'Peru'), ('Malawi', 'Malawi'), 
                ('Benin', 'Benin'), ('Sri-Lanka', 'Sri-Lanka'), ('Singapore', 'Singapore'), ("Cote-d'Ivoire", "Cote-d'Ivoire"), 
                ('Togo', 'Togo'), ('China', 'China'), ('Republic-of-Congo', 'Republic-of-Congo'), ('Sierra-Leone', 'Sierra-Leone'), 
                ('Burkina-Faso', 'Burkina-Faso'), ('Ukraine', 'Ukraine'), ('Ghana', 'Ghana'), ('Tonga', 'Tonga'), ('Libya', 'Libya'), 
                ('Indonesia', 'Indonesia'), ('Costa-Rica', 'Costa-Rica'), ('Mauritius', 'Mauritius'), ('Sweden', 'Sweden'), 
                ('Mali', 'Mali'), ('Russia', 'Russia'), ('United-Arab-Emirates', 'United-Arab-Emirates'), ('Angola', 'Angola'), 
                ('Chad', 'Chad'), ('Bosnia-and-Herzegovina', 'Bosnia-and-Herzegovina'), ('Burmese', 'Burmese'), ('US', 'US'), 
                ('Malaysia', 'Malaysia'), ('Senegal', 'Senegal'), ('Mozambique', 'Mozambique'), ('Uganda', 'Uganda'), ('Japan', 'Japan'), 
                ('Niger', 'Niger'), ('Brazil', 'Brazil'), ('United-Kingdom', 'United-Kingdom'), ('Guinea', 'Guinea'), ('Panama', 'Panama'),
                 ('Scotland', 'Scotland'), ('Ireland', 'Ireland'), ('Nigeria', 'Nigeria'), ('Ecuador', 'Ecuador'), ('Australia', 'Australia'),
                  ('Iran', 'Iran'), ('Algeria', 'Algeria'), ('Chile', 'Chile'), ('Belgium', 'Belgium'), ('Thailand', 'Thailand'), 
                  ('Haiti', 'Haiti'), ('Iraq', 'Iraq'), ('Georgia', 'Georgia'), ('Denmark', 'Denmark'), ('Poland', 'Poland'), ('New', 'New'), 
                  ('Morocco', 'Morocco'), ('Namibia', 'Namibia'), ('Guinea-Bissau', 'Guinea-Bissau'), ('Central-African-Republic', 'Central-African-Republic'), 
                  ('Estonia', 'Estonia'), ('Lebanon', 'Lebanon'), ('Tunisia', 'Tunisia'), ('Burundi', 'Burundi'), ('Nicaragua', 'Nicaragua'), 
                  ('Madagascar', 'Madagascar'), ('Dominican-Republic', 'Dominican-Republic'), ('Italy', 'Italy'), ('Sudan', 'Sudan'), 
                  ('Ivory-Coast', 'Ivory-Coast'), ('Maldives', 'Maldives'), ('Venezuela', 'Venezuela'), ('Israel', 'Israel'), 
                  ('Iceland', 'Iceland'), ('Zambia', 'Zambia'), ('Zimbabwe', 'Zimbabwe'), ('Democratic-Republic-of-Congo', 'Democratic-Republic-of-Congo'), 
                  ('Gambia', 'Gambia'), ('Kazakhstan', 'Kazakhstan'), ('Mauritania', 'Mauritania'), ('Kyrgyzstan', 'Kyrgyzstan'), 
                  ('Macedonia', 'Macedonia'), ('Latvia', 'Latvia'), ('Guyana', 'Guyana'), ('Syria', 'Syria'), ('Honduras', 'Honduras'), 
                  ('Trinidad-and-Tobago', 'Trinidad-and-Tobago'), ('Myanmar', 'Myanmar'), ('Mexico', 'Mexico'), ('Egypt', 'Egypt'), 
                  ('Cuba', 'Cuba'), ('Serbia', 'Serbia'), ('Democratic-Republic-of-the-Congo', 'Democratic-Republic-of-the-Congo'), 
                  ('Hong-Kong', 'Hong-Kong'), ('Greece', 'Greece'), ('Botswana', 'Botswana'), ('Bulgaria' , 'Bulgaria')]

class MyForm(Form):
    search_tweet = StringField("Hastag")
    # city = StringField("City")
    country = SelectField("Country", choices=country_list)
    participants = SelectField("# Participants", choices=participants_list)
    deaths = StringField("# Deaths")
    # injuries = StringField("# Injuries")
    target = SelectField("Target", choices=target_list)
    issue = SelectField("Issue", choices=issue_list)




@twitter.route('/')
def home():
    form = MyForm()
    return render_template('search_twitter.html', form = form)


@twitter.route('/submit', methods=('GET', 'POST'))
def submit():
    print '111'
    query = request.form['search_tweet']
    print '112'
    if(query == ""):
        return("no keyword")
    oauth_token = "802218282954747905-aibLqJnV93MWB8ZFEvhpQa5HTjNaNVX"
    oauth_token_secret = "lWnLP0MiJrNanfILvX48SerOXiiUYr9zo8UxnochCcqJz"
    app_key = "pLeOpV3TP1l3SGyNFjGfPUdgM"
    app_secret = "xoGYtBc2SujcWnWEDxNYd07Zv1MCTW57aBQVhwK90d0FhaqWIH"


    print '113'
    twitter = Twython(app_key=app_key, 
                app_secret=app_secret, 
                oauth_token=oauth_token, 
                oauth_token_secret=oauth_token_secret)
    print '114', query

    search = twitter.search(q=query,count=100)

    print '115'
    tweets = [ tweet['text'] for tweet in search['statuses']]
    # return(str(tweets))
    ##Changed here
    country = request.form['country']
    print '116'
    issue = int(request.form['issue'])

    print '117'
    v_rating = violence_rating(tweets)
    crime_rate = get_cr_based_on_country(country)
    target = int(request.form['target'])
    deaths = int(request.form['deaths'])
    npart = int(request.form['participants'])
    issue = int(request.form['issue'])
    
    values_list = [crime_rate,target,deaths,npart,v_rating,issue]
    riot_prob = str(calculate_riot_prob(values_list))
    return str(riot_prob)

def calculate_riot_prob(values_list):
    f = open(str(os.getcwd()) + '/app/predictor/rfmodel.pickle', 'rb')
    result = pickle.load(f)
    return result.predict_proba(values_list), result.predict(values_list) 


