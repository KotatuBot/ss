import os
import argparse
from gf_func import GF_Func


gf = GF_Func()

# args
exe_cute_dir = os.environ['PWD']
parser = argparse.ArgumentParser(description='Find word in file')

parser.add_argument('-d', help='file path')

args = parser.parse_args()


if args.d == None:
    args.d = "."
    gf.main(args.d)
else:
    gf.main(args.d)

    
