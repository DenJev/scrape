from scrape import TwitterApi
from scrape import TweetHolder
import sqlalchemy
# from scrape import cursor



def my_handler(event, context):
    search_params = {
        'q': 'ripple crypto',
        'result_type': 'recent',
        'count': 1000

    }

    #database_username = #
    #database_password = #
    #database_ip = #
    #database_name = #
    #database_connection = sqlalchemy.create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.
                                                   #format(database_username, database_password,
                                                     #     database_ip, database_name))

    #client_key = #
    #client_secret = #
    hello = TwitterApi(client_key, client_secret, search_params)
    hello.query(search_params)
    hello.query_to_class()
    hello.local_data.to_sql(con=database_connection, name='new_table', if_exists='append',
                            index=False)  # exports ram data scra
    database_connection.dispose()
my_handler('','')

