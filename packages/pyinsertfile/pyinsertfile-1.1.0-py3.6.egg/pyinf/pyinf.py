import argparse 

def main(): 

    parser = argparse.ArgumentParser(prog ='pyinf', description ='easy file inserting') 

    #parser.add_argument('mode',help='(pypi) for pypi package setup', required = False)
    parser.add_argument('mode', type=str)

    args = parser.parse_args()

    if args.mode:
        print(args.mode)

        if parser.mode == "pypi":
            print("demo")
        
            f = open("main.py","w+")

            f.write("""
            print("PyInsertFile")
            """)
