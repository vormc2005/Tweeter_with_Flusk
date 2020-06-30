from flask import Flask, render_template, session, redirect, request, url_for
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from user import User
from database import Database

app = Flask(__name__)
app.secret_key = '1234'
Database.initialize(user='postgres', password='Mysql#123', host='localhost', database='learning')


@app.route('/')  # http://127.0.0.1:4995
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():
    request_token = get_request_token()
    # Writing token to cookie, session
    session['request_token'] = request_token

    return redirect(get_oauth_verifier_url(request_token))
    # redirecting the user to Twitter so they can confirm authorization


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
    return render_template('profile.html', screen_name=session['screen_name'])


app.run(port=4995, debug=True)
