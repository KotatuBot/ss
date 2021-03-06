import re
import os
import subprocess
from terminaltables import AsciiTable
import termcolor

class GF_Func():
    def _init__(self):
        pass

    def filter_function(self,mode):
        if mode == "PHP":
            return ["for()","foreach()","COUNT()","SUM()","if()","elseif()","else()","array()","define()","while()"]

    def get_file_list(self):
        cmd = "find . -type f -print"
        file_list = subprocess.check_output(cmd.split()).decode('utf-8')
        file_dir = file_list.split('\n')
        return file_dir

    def filter_file(self,file_dir,pattern):
        filter_file_list = []
        if pattern == "php":
            filters = re.compile(r".php$")
        for files in file_dir:
            file_check = filters.findall(files)
            if len(file_check) != 0:
                filter_file_list.append(files)
        return filter_file_list



    def get_call_function(self,file_data_line,repattern):
        get_call_func = []
        file_check = repattern.findall(file_data_line)
        ffuction = self.filter_function("PHP")
        if len(file_check) > 0:
            for data in file_check:
                function_string = data + ")"
                if (function_string in ffuction) == False:
                    get_call_func.append(function_string)
        return get_call_func

    def get_def_function(self,file_data_line,repattern):
        get_user_func = []
        file_check = repattern.findall(file_data_line)
        hit_len = len(file_check)
        if hit_len>0:
                strip_func = file_data_line.strip('{\n')
                get_func   = strip_func.strip('function')
                get_user_func.append(get_func)
        return get_user_func

    def split_function(self,file_name):
        pwd = os.environ["PWD"]
        os_file_path = file_name.replace("./",pwd+"/")
        with open(os_file_path,'r') as fd:
            file_data = fd.readlines()

        call_func = []
        user_func = []
        file_dict = {}
        call_re_define   = re.compile(r'\w+\(')
        define_re_define = re.compile(r'^function\s*\w*\(')

        for data_tip in file_data:
            call_func_tmp = self.get_call_function(data_tip,call_re_define)
            user_func_tmp = self.get_def_function(data_tip,define_re_define)
            if len(call_func_tmp) != 0:
                for call_data in call_func_tmp:
                    call_func.append(call_data)

            if len(user_func_tmp) != 0:
                for user_data in user_func_tmp:
                    user_func.append(user_data)
        file_dict['Call_Func'] = call_func
        file_dict['Define_Func'] = user_func
        return file_dict,call_func,user_func


    def search_define(self,dict_data,function_name):
        # function_name
        source_name = []
        regex = re.compile(function_name.strip("()")+"\(")
        for sorce,value in dict_data.items():
            for value2 in value['Define_Func']:
                test = regex.findall(value2)
                if len(test) > 0:
                    source_name.append(sorce)
                    break
        return source_name

    def search_format(self,hit_source_name,function_name):

        if len(hit_source_name) != 0:
            head = []
            body = []
            all_table = []
            head.append("[Function Name]")
            head.append("[Define Source]")
            body.append(function_name)
            body.append(hit_source_name[0])
            all_table.append(head)
            all_table.append(body)
            table = AsciiTable(all_table)
            table.inner_row_border = True
            print(table.table)

        else:
            print("No Hit Function")

    def view_table(self,dict_name,func_list):
        func_all_list = []
        new_table_list = []
        for j in func_list:
            for t in j:
                ts = "".join(list(t)[1:])
                func_all_list.append(ts.split("(")[0]+"()")

        for source,value in dict_name.items():
            call_func_list = []
            for call_value in value['Call_Func']:
                if call_value in func_all_list:
                    create_func = call_value + " [M]"
                else:
                    create_func = call_value + " [O]"
                call_func_list.append(create_func)
            dict_name[source]['Call_Func'] = call_func_list

        for source_name,values in dict_name.items():
            tmp = []
            call_func_unique = list(set(values['Call_Func']))
            user_func_unique = list(set(values['Define_Func']))
            call_func_str = "\n".join(call_func_unique)
            user_func_str = "\n".join(user_func_unique)
            tmp.append(source_name)
            tmp.append(call_func_str)
            tmp.append(user_func_str)

            new_table_list.append(tmp)
        table = AsciiTable(new_table_list)
        table.inner_row_border = True
        print(table.table)

            

                    



    def main(self,path,mode="Normal",func_name="None"):
        if path != ".":
            filter_file_list = []
            filter_file_list.append(path)
        else:
            origin_file = self.get_file_list()
            filter_file_list = self.filter_file(origin_file,"php")
        all_file_dict = {}
        all_list = []
        user_all_list = []
        tmp = []
        tmp.append('File Name')
        tmp.append('Call FuncName')
        tmp.append('Define FuncName')
        all_list.append(tmp)
        for file_name in filter_file_list:
            tmp = []
            file_dict,call_func,user_func = self.split_function(file_name)

            all_file_dict[file_name]=file_dict
            call_func2 = list(set(call_func))
            user_func2 = list(set(user_func))

            if (len(call_func2)!=0 and len(call_func2)!= 0):
                if len(call_func2) == 0:
                    call_func2.append("NULL")
                if len(user_func2) == 0:
                    user_func2.append("NULL")


                call_func_str = "\n".join(call_func2)
                user_func_str = "\n".join(user_func2)


                tmp.append(file_name)
                tmp.append(call_func_str)
                tmp.append(user_func_str)
                all_list.append(tmp)
                all_file_dict[file_name] = file_dict

                if len(user_func) != 0 and mode=="Origin":
                    user_all_list.append(user_func)



        # View Table
        if mode == "Normal":
            table = AsciiTable(all_list)
            table.inner_row_border = True
            print(table.table)
        elif mode == "Search":
            hit_source = self.search_define(all_file_dict,func_name)
            self.search_format(hit_source,func_name)
        elif mode == "Origin":
            self.view_table(all_file_dict,user_all_list)



