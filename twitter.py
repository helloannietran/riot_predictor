from twython import Twython

#Variables that contains the user credentials to access Twitter API 
oauth_token = ""
oauth_token_secret = ""
app_key = ""
app_secret = ""


twitter = Twython(app_key=app_key, 
            app_secret=app_secret, 
            oauth_token=oauth_token, 
            oauth_token_secret=oauth_token_secret)

search = twitter.search(q='#ferguson',count=100)

tweets = search['statuses']

for tweet in tweets:
  # print(tweet['id_str'])
  print(tweet['text'])
