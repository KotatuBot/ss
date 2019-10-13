import re
import os
import subprocess
from terminaltables import AsciiTable
import termcolor


def get_file_list():
    cmd = "find . -type f -print"
    file_list = subprocess.check_output(cmd.split()).decode('utf-8')
    file_dir = file_list.split('\n')
    return file_dir

def filter_file(file_dir,pattern):
    filter_file_list = []
    if pattern == "php":
        filters = re.compile(r".php$")
    for files in file_dir:
        file_check = filters.findall(files)
        if len(file_check) != 0:
            filter_file_list.append(files)
    return filter_file_list



def get_call_function(file_data_line,repattern):
    get_call_func = []
    file_check = repattern.findall(file_data_line)
    if len(file_check) > 0:
        for data in file_check:
            get_call_func.append(data)
    return get_call_func

def get_def_function(file_data_line,repattern):
    get_user_func = []
    file_check = repattern.findall(file_data_line)
    hit_len = len(file_check)
    if hit_len>0:
            strip_func = file_data_line.strip('{\n')
            get_func   = strip_func.strip('function ')
            get_user_func.append(get_func)
    return get_user_func

def split_function(file_name):
    pwd = os.environ["PWD"]
    os_file_path = file_name.replace("./",pwd+"/")
    with open(os_file_path,'r') as fd:
        file_data = fd.readlines()

    call_func = []
    user_func = []
    file_dict = {}
    call_re_define   = re.compile(r'\w+\(\w+\);')
    define_re_define = re.compile(r'^function\s*\w*\(')


    for data_tip in file_data:
        call_func_tmp = get_call_function(data_tip,call_re_define)
        user_func_tmp = get_def_function(data_tip,define_re_define)
        if len(call_func_tmp) != 0:
            call_func.append(call_func_tmp[0])

        if len(user_func_tmp) != 0:
            user_func.append(user_func_tmp[0])

    file_dict['Call_Func'] = call_func
    file_dict['Define_Func'] = user_func
    return file_dict,call_func,user_func


def main():
    origin_file = get_file_list()
    filter_file_list = filter_file(origin_file,"php")
    all_file_dict = {}
    all_list = []
    tmp = []
    tmp.append('File Name')
    tmp.append('Call FuncName')
    tmp.append('Define FuncName')
    all_list.append(tmp)
    for file_name in filter_file_list:
        tmp = []
        file_dict,call_func,user_func = split_function(file_name)

        #all_file_dict[file_name]=file_dict
        call_func2 = list(set(call_func))
        user_func2 = list(set(user_func))

        if (len(call_func)!=0 and len(call_func)!= 0):
            if len(call_func2) == 0:
                call_func2.append("NULL")
            if len(user_func2) == 0:
                user_func2.append("NULL")


            file_name = termcolor.colored(file_name,"red")
            call_func_str = "\n".join(call_func2)
            user_func_str = "\n".join(user_func2)

            #call_func_str_c = termcolor.colored(call_func_str,"green")
            #user_func_str_c = termcolor.colored(user_func_str,"blue")

            tmp.append(file_name)
            tmp.append(call_func_str)
            tmp.append(user_func_str)
            all_list.append(tmp)

    table = AsciiTable(all_list)
    table.inner_row_border = True
    print(table.table)

main()
