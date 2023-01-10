#import modules
from decouple import config
from binance import ThreadedWebsocketManager
import psycopg2
import datetime

#generate API_KEY and API_SECRET from https://testnet.binance.vision
api_key = config("API_KEY")
api_secret = config("API_SECRET")

#your own password for the postgresql docker container
db_pass = config('DB_PASS')


def main():
    #connecting the timestampDB
    connection = psycopg2.connect(
        user='postgres',
        password=db_pass,
        host='127.0.0.1',
        port='5432',
        database='postgres'
    )

    cursor = connection.cursor()
    
    #to get info of multiple trades
    streams = ['ethbtc@trade', 'adabtc@trade']
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    twm.start()
    
    #a function that will store the info into the DB
    def handle_message(msg, cursor=cursor):
        print(msg)
        #a sample msg is:
        #{'stream': 'ethbtc@trade', 'data': {'e': 'trade', 'E': 1673349791225, 's': 'ETHBTC', 't': 396644796, 'p': '0.07711100', 'q': '0.09960000', 'b': 3417068429, 'a': 3417068824, 'T': 1673349791225, 'm': True, 'M': True}}
        #that is why we need msg['data'] of this dict. Here 't' is time, 's' is symbol, 'p' is price etc.
        #for more, check the binance python website
        
        msg = msg['data']
        query = "INSERT INTO raw_trade_data (TIME, SYMBOL, PRICE, QUANTITY)" +\
            "VALUES (%s,%s,%s,%s)"

        timestamp = datetime.datetime.fromtimestamp(int(msg['T']/1000))
        record_to_insert = (timestamp, msg['s'], msg['p'], msg['q'])
        cursor.execute(query, record_to_insert)
        connection.commit()


    twm.start_multiplex_socket(callback=handle_message, streams=streams)
    twm.join()

if __name__ == "__main__":
    main()
