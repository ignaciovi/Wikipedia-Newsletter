import psycopg2
import re
import logging
from config import config

def load_wikipedia_data(data):
    ''' Connect to the PostgreSQL database server '''

    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        print('Inserting data:')   
        cur.execute('INSERT INTO wiki_timebox_data (data) VALUES ('{}')'.format(data))
        print('Data inserted')
       
        cur.close()
        conn.commit()
        logging.debug('Inserted into database: {}'.format(data))
    except (Exception, psycopg2.DatabaseError) as error:
        logging.debug(error)
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
