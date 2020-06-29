# from database import connect
# from database import connection_pool
import json
import oauth2
from database import CursorConnectionFromPool
from twitter_utils import consumer



class User:
    def __init__(self, email, first_name, last_name, oauth_token, oauth_token_secret, id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return 'User {}'.format(self.email)

    def save_to_db(self):
        with CursorConnectionFromPool() as cursor:
            # Running code
            cursor.execute(
                'INSERT INTO users (email, first_name, last_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s, %s, %s)',
                (self.email, self.first_name, self.last_name, self.oauth_token, self.oauth_token_secret))
        # connection.commit()
        # connection_pool.putconn(connection)
        # connection.commit()
        # connection.close()

    @classmethod
    def load_from_db_by_email(cls, email):
        with CursorConnectionFromPool() as cursor:
            # connection = connection_pool.getconn()
            cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(email=user_data[1], first_name=user_data[2], last_name=[3],
                           oauth_token=user_data[4],
                           oauth_token_secret=user_data[5], id=user_data[0])

    def twitter_request(self, uri, verb='GET'):
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        # authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
        authorized_client = oauth2.Client(consumer, authorized_token)
        # Make Twitter API calls
        response, content = authorized_client.request(uri, verb)
        if response.status != 200:
            print("An error occurred when searching!")

        return json.loads(content.decode('utf-8'))


