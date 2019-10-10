import subprocess as sp
import os
import argparse
import re
from terminaltables import AsciiTable
import termcolor

def color_keyword(match_data,keyword,color):
    paint_color = termcolor.colored(keyword, color)
    color_match_data = match_data.replace(keyword,paint_color)
    return color_match_data


def data_arrange(stdout,keyword):

    data_all = []
    data_all.append(['File_Path','Number','Match'])
    current_path = os.environ['PWD']
    replace_path = stdout.replace(current_path,".")
    one_line = replace_path.split("\\n")

    for data in one_line:
        data_list = data.split(":")
        if len(data_list)==3:
            tmp = []
            strip_tab = data_list[2].replace("\\t","")
            strip_head = re.sub(r"^\s+",'',strip_tab)
            # I painted word
            color_filepath_data = color_keyword(data_list[0],data_list[0],'green')
            color_match_data = color_keyword(strip_head,keyword,'red')
            color_number = color_keyword(data_list[1],data_list[1],'blue')
            # append list
            tmp.append(color_filepath_data)
            tmp.append(color_number)
            tmp.append(color_match_data)
            data_all.append(tmp)
    return data_all



def table_view(data,keyword):
    if len(data) > 1:
        table = AsciiTable(data)
        print(table.table)
    else:

        err_message = termcolor.colored("\'"+keyword+"\'"+" did not hit", 'red')
        print(err_message)




def FileSearch(path,word,dir_path):

    if path!=".":
        full_path = dir_path + "/"+ path

    else:
        full_path = dir_path

    cmd = "find {0} -type f -print | xargs grep -n '{1}'".format(full_path,word)
    res = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
    stdout,strerr = res.communicate()
    data_str = str(stdout)
    data_s = data_arrange(data_str,word)
    table_view(data_s,word)



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
