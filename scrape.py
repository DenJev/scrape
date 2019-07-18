import base64
import requests
import pandas as pd
from datetime import datetime
import sqlalchemy


class TweetHolder:

    def __init__(self, text, created_at, favorite_count, retweet_count, lang, place, coordinates):

        self.text = text
        self.created_at = created_at
        self.favorite_count = favorite_count
        self.retweet_count = retweet_count
        self.lang = lang
        self.place = place
        self.coordinates = coordinates

    def date_format(self):

        self.created_at = datetime.strptime(self.created_at, '%a %b %d %H:%M:%S +0000 %Y')

class TwitterApi:

    def __init__(self, client_key, client_secret, search_params):

        self.__client_key = client_key
        self.__client_secret = client_secret
        print("Initialised client key and secret key")

        self.search_params = search_params

        # Formatting Keys
        print("formatting keys")
        self.__key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
        self.__b64_encoded_key = base64.b64encode(self.__key_secret)
        self.__b64_encoded_key = self.__b64_encoded_key.decode('ascii')
        print("keys formatted")

        # setting urls
        self._base_url = 'https://api.twitter.com/'
        self._auth_url = '{}oauth2/token'.format(self._base_url)

        # Here we obtain a bearer token for subsequent api requests
        auth_headers = {
            'Authorization': 'Basic {}'.format(self.__b64_encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

        auth_data = {
            'grant_type': 'client_credentials'
        }

        auth_resp = requests.post(self._auth_url, headers=auth_headers, data=auth_data)

        print("STATUS CODE FOR BEARER TOKEN REQUEST:", auth_resp.status_code)

        self.__access_token = auth_resp.json()['access_token']

        self.tweet_data = None

        self.local_data = None

    def initialise_database(self):

        #database_username = #
        #database_password = #
        #database_ip = #
        database_name = 'dbl'
        #database_connection = #

    def query(self, search_params):
        search_headers = {
            'Authorization': 'Bearer {}'.format(self.__access_token)
        }

        search_url = '{}1.1/search/tweets.json'.format(self._base_url)

        search_resp = requests.get(search_url, headers=search_headers, params=search_params)

        self.tweet_data = search_resp.json()

        print(self.tweet_data)

    def query_to_pandas(self):

        list_created_at = []  # initialising lists
        list_id = []
        list_text = []

        number_of_tweets = len(self.tweet_data['statuses'])  # setting the number of requests captured in the request
        for i in range(0, number_of_tweets - 1):

            list_created_at.append(self.tweet_data['statuses'][i]['created_at'])
            list_id.append(self.tweet_data['statuses'][i]['id'])
            list_text.append(self.tweet_data['statuses'][i]['text'])
        #  Data frame stored locally of tweets
        self.local_data = pd.DataFrame({'created_at': list_created_at, 'id': list_id, 'text': list_text})

        print(self.local_data)

    def query_to_class(self):

        number_of_tweets = len(self.tweet_data['statuses'])
        query_objects = []
        list_text = []
        list_created_at = []
        list_favorite_count = []
        list_retweet_count = []
        list_lang = []
        list_place = []
        list_coordinates = []
        for i in range(0, number_of_tweets - 1):
            tweet_holder = TweetHolder(self.tweet_data['statuses'][i]['text'],
                                       self.tweet_data['statuses'][i]['created_at'],
                                       self.tweet_data['statuses'][i]['favorite_count'],
                                       self.tweet_data['statuses'][i]['retweet_count'],
                                       self.tweet_data['statuses'][i]['lang'],
                                       self.tweet_data['statuses'][i]['place'],
                                       self.tweet_data['statuses'][i]['coordinates'])

            tweet_holder.date_format()
            list_text.append(tweet_holder.text)
            list_created_at.append(tweet_holder.created_at)
            list_favorite_count.append(tweet_holder.favorite_count)
            list_retweet_count.append(tweet_holder.retweet_count)
            list_lang.append(tweet_holder.lang)
            list_place.append(tweet_holder.place)
            list_coordinates.append(tweet_holder.coordinates)
            query_objects.append(tweet_holder)
        self.local_data = pd.DataFrame({'text': list_text,
                                        'created_at': list_created_at,
                                        'favorite_count': list_favorite_count,
                                        'retweet_count': list_retweet_count,
                                        'lang': list_lang,
                                        })
        print(self.local_data)


