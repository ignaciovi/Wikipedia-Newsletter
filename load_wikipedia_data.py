import psycopg2
import re
import logging
from config import config

def load_wikipedia_data(data):
    ''' Connect to the PostgreSQL database server '''

    logging.basicConfig(filename='logs/etl.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)

    conn = None
    try:
        params = config()

        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        logging.info('Inserting data:')   
        cur.execute('INSERT INTO wiki_timebox_data (data) VALUES ('{}')'.format(data))
        logging.info('Data inserted')
       
        cur.close()
        conn.commit()
        logging.info('Inserted into database: {}'.format(data))
    except (Exception, psycopg2.DatabaseError) as error:
        logging.exception(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
