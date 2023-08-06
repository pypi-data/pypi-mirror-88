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

cmd: pyinf
>> mode: [(pypi): pypi package setup, (none, clear, anything else): main.py file] : --- at here enter the mode ---
for example pypi mode
>> package name: -- enter package name --
for example pyinsertfileTutorial
>> author name: -- enter your name --
for example author
finished now you have your package example you should fill it as your own

  
# FIXES
 
 fixed must of bugs
 this is stable version
 
# CONTACT
 
 mirzaeiariya88@gmail

"""

setup( 
		name ='pyinsertfile', 
		version ='1.3', 
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
