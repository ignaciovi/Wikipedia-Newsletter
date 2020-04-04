import time
from retrieve_wikipedia_info import retrieve_wikipedia_info
from transform_wikipedia_data import transform_wikipedia_data
import luigi


# Task A
# Fetch data from wikipedia and store it in file
# Task A - write hello world in text file
class HelloWorld(luigi.Task):
    def requires(self):
        return None
 
    def output(self):
        return luigi.LocalTarget('wikipedia_info_api.txt')
 
    def run(self):
        html_content = retrieve_wikipedia_info()
        with self.output().open('w') as outfile:
            outfile.write(html_content)

# Task B
# Retrieve data from html file
class NameSubstituter(luigi.Task):
    def requires(self):
        return HelloWorld()

    def output(self):
        return luigi.LocalTarget('wikipedia_info_output.txt')

    def run(self):
        with self.input().open() as infile, self.output().open('w') as outfile:
            text = infile.read()
            output_text = transform_wikipedia_data(text)
            outfile.write(output_text)


if __name__ == '__main__':
    luigi.run()
