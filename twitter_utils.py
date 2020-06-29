import oauth2
import constants
import urllib.parse as urlparse

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


def get_request_token():
    # Create consumer, who uses CONSUMER_KEY, CONSUMER_SECRET to adentify app uniquely
    client = oauth2.Client(consumer)
    # Use client to perform a request for the request token
    # send request to get a token
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print('An error occured getting the request token from Twitter')
    # get request token parsing the query string returned
    # parsing information from bytes to a string
    return dict(urlparse.parse_qsl(content.decode('utf-8')))


def get_oauth_verifier(request_token):
    # Ask the user to get a pin code and authorize
    print('Go to the following site in your browser: ')
    print('{}?oauth_token={}'.format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

    return input("What is the Pin? ")


def get_access_token(request_token, oauth_verifier):
    # create token Objject that contains the request token and verifier

    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    # create client with our consumer and the newly created and verified token
    client = oauth2.Client(consumer, token)
    # Ask tweeter fir an access token, and Twitter knows it should give us it because we've verified the request
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))
