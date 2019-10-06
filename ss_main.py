import subprocess as sp
import os
import argparse

def FileSearch(path,word,dir_path):

    if path!=".":
        full_path = dir_path + "/"+ path

    else:
        full_path = dir_path

    cmd = "find {0} -type f -print | xargs grep -n '{1}'".format(full_path,word)
    res = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
    stdout,strerr = res.communicate()
    print(stdout)



# args
exe_cute_dir = os.environ['PWD']
parser = argparse.ArgumentParser(description='Find word in file')

parser.add_argument('-d', help='file path')
parser.add_argument('-s', help='Search Keyword')

args = parser.parse_args()


if (args.d!=None and len(args.s)!=None):
       FileSearch(args.d,args.s,exe_cute_dir) 
else:
    print("Please set an argument")
    print("-d: Directory or file path")
    print("-s : Find word")
