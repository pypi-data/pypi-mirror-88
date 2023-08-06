from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()
    
setup(	name = 'alpacka',
      	version = '0.0.44',
     	description = 'The alpacka Python package, used to extract and visualize metadata from text data sets',
      	author = 'Fredrik Möller',
      	author_email = 'fredrikmoller@recordefuture.com',
      	long_description = readme(),
      	long_description_content_type = 'text/markdown',
      	url = 'https://github.com/BernhardMoller/alpacka',
      	packagages = ['pipes', 'functions', 'demos'],
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    	],
	licence = 'MIT', 
	python_requires='>=3.6',
      )

 