from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='alpacka',
      version='0.0.45',
      description='The alpacka Python package, used to extract and visualize metadata from text data sets',
      author='Fredrik Möller',
      author_email='fredrikmoller@recordefuture.com',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://github.com/BernhardMoller/alpacka',
      packagages=['pipes'
                  'pipes.data_loader',
                  'pipes.ncof_pipeline',
                  'pipes.tfidf_pipeline',
                  'functions',
                  'functions.presentation_functions'
                  'functions.statistic_methods'],
      licence='LICENCE.txt',
      python_requires='>=3.6',
      )
