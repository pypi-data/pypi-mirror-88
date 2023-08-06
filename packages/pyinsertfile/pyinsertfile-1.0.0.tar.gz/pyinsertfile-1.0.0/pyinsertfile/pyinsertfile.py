import argparse 

def main(): 

    parser = argparse.ArgumentParser(prog ='pyinf', description ='pyinsertfile easy file package') 

    args = parser.parse_args()

    f = open("main.py","w+")

    f.write("""
    print("PyInsertFile")
    """)
