# from database import connect
# from database import connection_pool
import json
import oauth2
from database import CursorConnectionFromPool
from twitter_utils import consumer



class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return 'User {}'.format(self.screen_name)

    def save_to_db(self):
        with CursorConnectionFromPool() as cursor:
            # Running code
            cursor.execute(
                'INSERT INTO users (screen_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s)',
                ( self.screen_name, self.oauth_token, self.oauth_token_secret))
        # connection.commit()
        # connection_pool.putconn(connection)
        # connection.commit()
        # connection.close()

    @classmethod
    def load_from_db_by_screen_name(cls, screen_name):
        with CursorConnectionFromPool() as cursor:
            # connection = connection_pool.getconn()
            cursor.execute('SELECT * FROM users WHERE screen_name=%s', (screen_name,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(screen_name=user_data[1],
                           oauth_token=user_data[2],
                           oauth_token_secret=user_data[3], id=user_data[0])

    def twitter_request(self, uri, verb='GET'):
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        # authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
        authorized_client = oauth2.Client(consumer, authorized_token)
        # Make Twitter API calls
        response, content = authorized_client.request(uri, verb)
        if response.status != 200:
            print("An error occurred when searching!")

        return json.loads(content.decode('utf-8'))


