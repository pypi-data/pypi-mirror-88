import argparse
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
            print("pkg name set as default(test)")
        else:
            print("pkg name set as " + pn)
            
            f = open("setup.py","w+")

            f.write("""print("Test Setup")""")
            
            os.mkdir(str(pn))
    else:
        printProgressBar(0, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
        f = open("main.py","w+")

        f.write("""print("PyInsertFile")""")
        
        printProgressBar(100, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
