import os
import argparse
from gf_func import GF_Func


gf = GF_Func()

# args
exe_cute_dir = os.environ['PWD']
parser = argparse.ArgumentParser(description='Analysis function in Source')

parser.add_argument('-d', help='file path\n example: index.php\ndefault is current_dir')
parser.add_argument('-s', help='Search func')

args = parser.parse_args()


if args.s != None:
    gf.main(".",mode="Search",func_name=args.s)
elif args.d == None:
    args.d = "."
    gf.main(args.d)
else:
    gf.main(args.d)

    
