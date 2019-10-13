import os
import argparse
from gf_func import GF_Func


gf = GF_Func()

# args
exe_cute_dir = os.environ['PWD']
parser = argparse.ArgumentParser(description='Analysis function in Source')

parser.add_argument('-d', help='file path\n example: index.php\ndefault is current_dir')
parser.add_argument('-m', help="mode -> o,s")
parser.add_argument('-s', help="search function name")

args = parser.parse_args()

if args.m != None:
    if args.m == "o":
        gf.main(".",mode="Origin")
    elif args.m == "s" and args.s!=None:
        gf.main(".",mode="Search",func_name=args.s)
elif args.d == None:
    args.d = "."
    gf.main(args.d)
else:
    gf.main(args.d)

    
