import time
from retrieve_wikipedia_info import retrieve_wikipedia_info
from transform_wikipedia_data import transform_wikipedia_data
from load_wikipedia_data import load_wikipedia_data
import luigi


# Task A
# Fetch data from wikipedia and store it in file
class RetrieveWikipediaData(luigi.Task):
    def requires(self):
        return None
 
    def output(self):
        return luigi.LocalTarget('wikipedia_info_api3.txt')
 
    def run(self):
        html_content = retrieve_wikipedia_info()
        with self.output().open('w') as outfile:
            outfile.write(html_content)

# Task B
# Retrieve data from html file
class TransformWikipediaData(luigi.Task):
    def requires(self):
        return RetrieveWikipediaData()

    def output(self):
        return luigi.LocalTarget('wikipedia_info_output3.txt')

    def run(self):
        with self.input().open() as infile, self.output().open('w') as outfile:
            text = infile.read()
            output_text = transform_wikipedia_data(text)
            outfile.write(output_text)

# Retrieve data from html file
class LoadWikipediaData(luigi.Task):
    def requires(self):
        return TransformWikipediaData()

    def output(self):
        return luigi.LocalTarget('wikioutput.txt')

    def run(self):
        with self.input().open() as infile, self.output().open('w') as outfile:
            text = infile.read()
            load_wikipedia_data(text)
            outfile.write("Success")

            
if __name__ == '__main__':
    luigi.run()
