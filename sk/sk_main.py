import os
import argparse
from searchkey import SearchKey

sk = SearchKey()

# args
exe_cute_dir = os.environ['PWD']
parser = argparse.ArgumentParser(description='Find word in file')

parser.add_argument('-d', help='file path')
parser.add_argument('-s', help='Search Keyword')
parser.add_argument('-m',help='open vim mode\n(example: -m vim)')

args = parser.parse_args()


if (len(args.s)!=None and args.m==None):
    if args.d == None:
        args.d = "."
    sk.FileSearch(args.d,args.s,exe_cute_dir,"no") 
elif (len(args.s)!=None and args.m=="vim"):
    if args.d == None:
        args.d = "."
    sk.FileSearch(args.d,args.s,exe_cute_dir,"vim") 
else:
    print("Please set an argument")
    print("-d: Directory or file path")
    print("-s : Find word")
    print("-m: Open vim")
