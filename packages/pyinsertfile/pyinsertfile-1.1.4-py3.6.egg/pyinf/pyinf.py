import argparse 

def main(): 

    parser = argparse.ArgumentParser(prog ='pyinf', description ='easy file inserting') 

    
    args = parser.parse_args()

    
    m = input("mode: [(pypi): pypi package setup, (none, clear, anything else): main.py file]")
    
    if m == "pypi":
        pn = input(" >> package name : ")
        
        if pn == "":
            print("pkg name set as default(test)")
        else:
            print("pkg name set as " + pn)
    else:
        f = open("main.py","w+")

        f.write("""print("PyInsertFile")""")
