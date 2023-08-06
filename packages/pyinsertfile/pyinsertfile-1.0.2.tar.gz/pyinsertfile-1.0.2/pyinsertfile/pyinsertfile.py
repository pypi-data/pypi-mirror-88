import argparse 

def main(): 

    parser = argparse.ArgumentParser(prog ='asdasd', description ='easy file inserting') 

    args = parser.parse_args()

    f = open("main.py","w+")

    f.write("""
    print("PyInsertFile")
    """)
