import re
from terminaltables import AsciiTable
from terminal import Terminal,InquirerControl
from terminal2 import TEST
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

    def mode_data(self,stdout):

        data_all = []
        match_dict = {}
        current_path = os.environ['PWD']
        one_line = stdout.split("\\n")

        for data in one_line:
            data_list = data.split(":")
            if len(data_list)==3:
                tmp = []
                strip_tab = data_list[2].replace("\\t","")
                strip_head = re.sub(r"^\s+",'',strip_tab)
                # append list
                absolte_path = data_list[0]
                relative_path = data_list[0].replace(current_path,".")
                tmp.append(relative_path+":"+data_list[1])
                tmp.append(absolte_path)
                match_dict[relative_path+":"+data_list[1]] = strip_head
                data_all.append(tmp)
        return data_all,match_dict



    def table_view(self,data,keyword):
        if len(data) > 1:
            table = AsciiTable(data)
            print(table.table)
        else:

            err_message = termcolor.colored("\'"+keyword+"\'"+" did not hit", 'red')
            print(err_message)

    def CommandTerminal(self,file_name,dict_name):
        a = TEST(dict_name)
        while 1:
            a.main(file_name)
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
        data_s = self.data_arrange(data_str,word)
        if mode == "vim":
            if len(data_s)!=0:
                mode_file_data,mode_dict_data = self.mode_data(data_str)
                self.CommandTerminal(mode_file_data,mode_dict_data)
        else:
            self.table_view(data_s,word)


