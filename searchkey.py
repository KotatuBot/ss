import re
from terminaltables import AsciiTable
from terminal import TerminalView
import subprocess as sp
import os
import termcolor



class SearchKey():

    def __init__(self):
        pass

    def color_keyword(self,match_data,keyword,color):
        paint_color = termcolor.colored(keyword, color)
        color_match_data = match_data.replace(keyword,paint_color)
        return color_match_data


    def data_arrange(self,stdout,keyword):

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
                color_filepath_data = self.color_keyword(data_list[0],data_list[0],'green')
                color_match_data = self.color_keyword(strip_head,keyword,'red')
                color_number = self.color_keyword(data_list[1],data_list[1],'blue')
                # append list
                tmp.append(color_filepath_data)
                tmp.append(color_number)
                tmp.append(color_match_data)
                data_all.append(tmp)
        return data_all

    def max_counter(self,one_line):
        current_path = os.environ['PWD']
        tmp = []
        for data in one_line:
            data_list = data.split(":")
            if len(data_list)==3:
                strip_tab = data_list[2].replace("\\t","")
                strip_head = re.sub(r"^\s+",'',strip_tab)
                # append list
                relative_path = data_list[0].replace(current_path,".")
                tmp.append(len(relative_path+":"+data_list[1]))
        max_length = max(tmp)
        return max_length

    def mode_data(self,stdout):

        data_all = []
        current_path = os.environ['PWD']
        one_line = stdout.split("\\n")
        max_length = self.max_counter(one_line)
        for data in one_line:
            data_list = data.split(":")
            if len(data_list)==3:
                tmp = []
                strip_tab = data_list[2].replace("\\t","")
                strip_head = re.sub(r"^\s+",'',strip_tab)
                # append list
                absolte_path = data_list[0]
                relative_path = data_list[0].replace(current_path,".")
                relative_path_len = len(relative_path+":"+data_list[1])
                spach_count = max_length - relative_path_len 
                blank = ""
                for i in range(spach_count):
                    blank += " "
                rpd = relative_path+":"+data_list[1] + blank +"| "+strip_head
                tmp.append(rpd)
                tmp.append(absolte_path)
                data_all.append(tmp)

        return data_all



    def table_view(self,data,keyword):
        if len(data) > 1:
            table = AsciiTable(data)
            print(table.table)
        else:

            err_message = termcolor.colored("\'"+keyword+"\'"+" did not hit", 'red')
            print(err_message)

    def CommandTerminal(self,file_name):
        tv = TerminalView()
        while 1:
            tv.main(file_name)
            continue_key = input("Continue?[y/n]")
            if(continue_key == "n"):
                break

    def FileSearch(self,path,word,dir_path,mode):

        if path!=".":
            full_path = dir_path + "/"+ path

        else:
            full_path = dir_path

        cmd = "find {0} -type f -print | xargs grep -n '{1}'".format(full_path,word)
        res = sp.Popen(cmd, shell=True, stdout=sp.PIPE)
        stdout,strerr = res.communicate()
        data_str = str(stdout)
        if mode == "vim":
            if len(data_str)!=0:
                mode_file_data = self.mode_data(data_str)
                self.CommandTerminal(mode_file_data)
        else:
            data_s = self.data_arrange(data_str,word)
            self.table_view(data_s,word)


