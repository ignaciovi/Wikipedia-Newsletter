import time
import luigi
import psycopg2
import csv
import time
from datetime import datetime
from retrieve_wikipedia_info import retrieve_wikipedia_info
from transform_wikipedia_data import transform_wikipedia_data
from load_wikipedia_data import load_wikipedia_data
from luigi.contrib.postgres import PostgresTarget
from csv import reader
from luigi.format import UTF8
from config import config


# Task A
# Fetch data from wikipedia and store it in file
class RetrieveWikipediaInfo(luigi.Task):
    def requires(self):
        return None
 
    def output(self):
        return luigi.LocalTarget('wikipedia_info_api.txt', format=UTF8)
 
    def run(self):
        wikipedia_info_content = retrieve_wikipedia_info()
        with self.output().open('w') as outfile:
            outfile.write(wikipedia_info_content)

# Task B
# Retrieve data from html file
class TransformWikipediaInfo(luigi.Task):
    def requires(self):
        return RetrieveWikipediaInfo()

    def output(self):
        return luigi.LocalTarget('wikipedia_info_output.csv')

    def run(self):
        with self.input().open() as infile, self.output().open('wb') as outfile:
            fieldnames = ['year', 'event']
            writer = csv.DictWriter(outfile, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
            writer.writeheader()
            text = infile.read()
            output_array= transform_wikipedia_data(text)
            for el in output_array:
                writer.writerow({'year': el[0], 'event': el[1]})

class LoadWikipediaInfoSQL(luigi.Task):
    def requires(self):
        return TransformWikipediaInfo()
        
    def output(self):
        params = config()
        return PostgresTarget(
            **params
        )

    def  run(self):
        output=self.output()
        connection = output.connect()
        connection.set_client_encoding('UTF8')
        cursor = connection.cursor()

        with self.input().open() as infile:
            csv_reader = reader(infile)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                if row[1] != "event":
                    query = u"INSERT INTO wikitimeboxdata (year, event) VALUES ('{}', '{}')".format(row[0], row[1].replace("'", ""))
                    cursor.execute(query)

                    # Update marker table
                    self.output().touch(connection)

                # commit and close connection
                connection.commit()
            connection.close()


            
if __name__ == '__main__':
    luigi.run()
