import argparse 

def main(): 

    parser = argparse.ArgumentParser(prog ='pyinf', description ='easy file inserting') 

    #parser.add_argument('mode',help='(pypi) for pypi package setup', required = False)
    parser.add_argument('mode', type=str, help="(pypi) for pypi package setup, (anything else) main.py file")

    args = parser.parse_args()

    if args.mode:
        print(args.mode)
        print("")

        if args.mode == "pypi":
            print("demo")
        else:
            f = open("main.py","w+")

            f.write("""
            print("PyInsertFile")
            """)
