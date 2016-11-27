from twython import Twython

#Variables that contains the user credentials to access Twitter API 
# oauth_token = ""
# oauth_token_secret = ""
# app_key = ""
# app_secret = ""

oauth_token = "802218282954747905-aibLqJnV93MWB8ZFEvhpQa5HTjNaNVX"
oauth_token_secret = "lWnLP0MiJrNanfILvX48SerOXiiUYr9zo8UxnochCcqJz"
app_key = "pLeOpV3TP1l3SGyNFjGfPUdgM"
app_secret = "xoGYtBc2SujcWnWEDxNYd07Zv1MCTW57aBQVhwK90d0FhaqWIH"

def get_tweets(hashtag):
	twitter = Twython(app_key=app_key, 
	            app_secret=app_secret, 
	            oauth_token=oauth_token, 
	            oauth_token_secret=oauth_token_secret)

	search = twitter.search(q=hashtag,count=100)

	tweets = search['statuses']

	# text = tweets['text']
	texts = [tweet['text'] for tweet in tweets]
	return texts
# print get_tweets("#happy")
# for tweet in tweets:
#   # print(tweet['id_str'])
#   print(tweet['text'])
