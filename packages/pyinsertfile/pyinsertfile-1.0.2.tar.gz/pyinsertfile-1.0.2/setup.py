from setuptools import setup, find_packages 

with open('requirements.txt') as f: 
	requirements = f.readlines() 

long_description = """
# DESCRIPTION

for making main.py files with just pyinf in your cmd

# USAGE

 - pyinf

"""

setup( 
		name ='pyinsertfile', 
		version ='1.0.2', 
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
				'pyinsertfile = pyinsertfile.pyinsertfile:main'
			] 
		}, 
		classifiers =( 
			"Programming Language :: Python :: 3", 
			"License :: OSI Approved :: MIT License", 
			"Operating System :: OS Independent", 
		), 
		keywords ='Easy file', 
		install_requires = requirements, 
		zip_safe = False
) 
