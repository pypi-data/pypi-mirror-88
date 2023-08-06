from setuptools import setup, find_packages 

with open('requirements.txt') as f: 
	requirements = f.readlines() 

long_description = """
# DESCRIPTION

for making main.py files with just pyinf in your cmd

pyinsertfile have to option pypi, none or anything else
pypi option will make a package setup for you pypi package
none or anything else option will generate main.py

leave it nothing to generate main.py

# USAGE

 - pyinf
  - mode
 
# EXAMPLES

 - pyinf - 
  - enter mode -
   - if pypi mode -
  - package name -
   - none mode -
  - generates main.py file
  
# FIXES
 
 fixed must of bugs
 
# CONTACT
 
 mirzaeiariya88@gmail

"""

setup( 
		name ='pyinsertfile', 
		version ='1.2', 
		author ='Ariya Mirzaei', 
		author_email ='mirzaeiariya88@gmail.com', 
		url ='https://github.com/Ariya1234gamer', 
		description ='Package for making main.py files', 
		long_description = long_description, 
		long_description_content_type ="text/markdown", 
		license ='MIT', 
		packages = find_packages(), 
		entry_points ={ 
			'console_scripts': [ 
				'pyinf = pyinf.pyinf:main'
			] 
		}, 
		classifiers =( 
			"Programming Language :: Python :: 3", 
			"License :: OSI Approved :: MIT License", 
			"Operating System :: OS Independent", 
		), 
		keywords ='Easy file', 
		install_requires = ["argparse"] ,
		zip_safe = False
) 
