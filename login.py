
from user import User
from database import Database
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token

Database.initialize(user='postgres', password='Mysql#123', host='localhost', database='learning')

user_email = input("Enter your e-mail address: ")
user = User.load_from_db_by_email(user_email)

if not user:
    # get request token parsing the query string returned
    # parsing information from bytes to a string
    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    # create token Objject that contains the request token and verifier

    access_token = get_access_token(request_token, oauth_verifier)

    # print(access_token)
    # Create an "authorized_token" Token object and use to perform Twitter API calls on behalf of the user

    # Uploading user to PostgreSQL
    # email = input("Enter your email: ")

    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'],
                None)
    user.save_to_db()

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')

for tweet in tweets['statuses']:
    print(tweet['text'])
