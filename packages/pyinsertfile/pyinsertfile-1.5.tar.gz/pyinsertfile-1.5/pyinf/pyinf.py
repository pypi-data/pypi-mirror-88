import argparse
from datetime import datetime
import os

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

def main(): 
    parser = argparse.ArgumentParser(prog ='pyinf', description ='easy file inserting')
    
    args = parser.parse_args()
    
    m = input(" >> mode: [(pypi): pypi package setup, (none, clear, anything else): main.py file] : ")
    
    if m == "pypi":
        pn = input(" >> package name : ")
        
        if pn == "":
            print("FAILED")
        else:
            print("pkg name set as " + pn)
            
            s = open("setup.py","w+")
            
            os.mkdir(str(pn))
            
            auth = input(" >> author : ")
            
            if auth == "":
                print("FAILED")
            else:
                print("author name set as " + auth)
                
                s.write("""from setuptools import setup, find_packages 

long_description = '''
# DESCRIPTION

PyInsertFile Generated Packagep

'''

setup( 
		name ='""" + pn +"""', 
		version ='1.0.0', 
		author ='""" + auth +"""', 
		author_email ='example@example.com', 
		url ='https://example.com', 
		description ='PyInsertFile Generated Package', 
		long_description = long_description, 
		long_description_content_type ="text/markdown", 
		license ='MIT', 
		packages = find_packages(), 
		entry_points ={ 
			'console_scripts': [ 
				'""" + pn + """ = """ + pn + """.""" + pn + """:main'
			] 
		}, 
		classifiers =( 
			"Programming Language :: Python :: 3", 
			"License :: OSI Approved :: MIT License", 
			"Operating System :: OS Independent", 
		), 
		keywords ='PyInsertFile Generated Package', 
		install_requires = [] ,
		zip_safe = False
) 
""")
                
                l = open("LICENSE","w+")

                l.write(
                """  
MIT License

Copyright (c) 2020 """ + auth + """

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
                )
                
                r = open("README.md","w+")

                r.write("UNKNOWN")
                
                init = open(pn + "\\__init__.py", "w+")
                file = open(pn + "\\" + pn + ".py", "w+")
                
    else:
        printProgressBar(0, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
        f = open("main.py","w+")

        f.write("""print("PyInsertFile")""")
        
        printProgressBar(100, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
