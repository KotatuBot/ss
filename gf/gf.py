import re
import os
import subprocess

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
    return file_dict


def main():
    origin_file = get_file_list()
    filter_file_list = filter_file(origin_file,"php")
    all_file_dict = {}
    for file_name in filter_file_list:
        file_dict = split_function(file_name)
        all_file_dict[file_name]=file_dict


    for source,value in all_file_dict.items():
        if (len(value['Call_Func'])!=0 or len(value['Define_Func'])!=0):
            print("Source Path: "+source)
            print("Call_Func: "+",".join(value['Call_Func']))
            print("Define_Func: "+",".join(value['Define_Func']))
            print("--------")

main()
