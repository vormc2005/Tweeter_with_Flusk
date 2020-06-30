from flask import Flask, render_template, session, redirect, request, url_for, g
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from user import User
from database import Database
import requests

app = Flask(__name__)
app.secret_key = '1234'
Database.initialize(user='postgres', password='Mysql#123', host='localhost', database='learning')


@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_from_db_by_screen_name(session['screen_name'])


@app.route('/')  # http://127.0.0.1:4995
def homepage():
    return render_template('home.html')
    # return redirect('login/twitter')


@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    request_token = get_request_token()
    # Writing token to cookie, session
    session['request_token'] = request_token

    return redirect(get_oauth_verifier_url(request_token))
    # redirecting the user to Twitter so they can confirm authorization


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/auth/twitter')  # http://127.0.0.1:4995/auth/twitter?oauth_verifier=123456
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'], None)
        user.save_to_db()

    session['screen_name'] = user.screen_name

    # return user.screen_name
    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    # return render_template('profile.html', screen_name=session['screen_name'])
    return render_template('profile.html', user=g.user)


@app.route('/search')
def search():
    query = request.args.get('q')
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))

    tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']]
    for tweet in tweet_texts:
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label
    return render_template('search.html', content=tweet_texts)


app.run(port=4995, debug=True)
