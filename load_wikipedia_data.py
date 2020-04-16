import psycopg2
from config import config
import re

def load_wikipedia_data(data):
    ''' Connect to the PostgreSQL database server '''

    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
        
        
        print('Inserting data:')   
        cur.execute('INSERT INTO wiki_timebox_data (data) VALUES ('{}')'.format(data))
        print('Data inserted')
       
       # close the communication with the PostgreSQL
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
