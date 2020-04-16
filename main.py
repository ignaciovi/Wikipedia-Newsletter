import time
import csv
import luigi
import logging
from datetime import datetime
from retrieve_wikipedia_info import retrieve_wikipedia_info
from transform_wikipedia_data import transform_wikipedia_data
from luigi.contrib.postgres import PostgresTarget
from csv import reader
from luigi.format import UTF8
from config import config
from luigi.contrib.s3 import S3Target, S3Client
from time import strftime

logging.basicConfig(filename='logs/etl.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.DEBUG)

# Task A
# Fetch data from wikipedia and store it in txt file
class RetrieveWikipediaInfo(luigi.Task):
    def requires(self):
        return None
 
    def output(self):
        params = config(section='s3')
        client = S3Client(**params)
        return S3Target('s3://s3-bucket-wikidata/{}/wikipedia_info_api.txt'.format(strftime('%Y-%m-%d')), format=UTF8, client=client)
 
    def run(self):
        logging.info('Running RetrieveWikipediaInfo')
        wikipedia_info_content = retrieve_wikipedia_info()
        with self.output().open('w') as outfile:
            outfile.write(wikipedia_info_content)

# Task B
# Clean data, retrieve event information and store in csv file
class TransformWikipediaInfo(luigi.Task):
    def requires(self):
        return RetrieveWikipediaInfo()

    def output(self):
        params = config(section='s3')
        client = S3Client(**params)
        return S3Target('s3://s3-bucket-wikidata/{}/wikipedia_info_output.csv'.format(strftime('%Y-%m-%d')), format=UTF8, client=client)

    def run(self):
        logging.info('Running TransformWikipediaInfo')
        with self.input().open() as infile, self.output().open('w') as outfile:
            fieldnames = ['year', 'event']
            writer = csv.DictWriter(outfile, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
            writer.writeheader()
            text = infile.read()
            output_array= transform_wikipedia_data(text)
            for el in output_array:
                writer.writerow({'year': el[0], 'event': el[1]})

# Task C
# Load csv file from previous task into an SQL database
class LoadWikipediaInfoSQL(luigi.Task):
    def requires(self):
        return TransformWikipediaInfo()
        
    def output(self):
        params = config(section='postgresql')
        return PostgresTarget(**params)

    def  run(self):
        logging.info('Running LoadWikipediaInfoSQL')
        logging.info('Connecting to the PostgreSQL database...')
        output=self.output()
        connection = output.connect()
        connection.set_client_encoding('UTF8')
        cursor = connection.cursor()

        with self.input().open() as infile:
            csv_reader = reader(infile)
            for row in csv_reader:
                if row[1] != 'event':
                    query = u'INSERT INTO wiki_timebox_data (year, event) VALUES ('{}', '{}')'.format(row[0], row[1].replace("'", ""))
                    cursor.execute(query)
                    self.output().touch(connection)

                connection.commit()
                logging.info('Row inserted')
            connection.close()
            logging.info('Database connection closed.')
          
if __name__ == '__main__':
    logging.info('Running pipeline')
    luigi.run()
