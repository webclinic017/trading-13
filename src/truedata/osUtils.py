import sys
import os


class osUtils:
    def __init__(self):
        pass

    def write_text_to_file(self, filename, text):
        if os.path.exists(filename):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not

        print("WRITING TO FILE")
        f = open(filename, append_write)
        f.write(text)
        f.close

    def read_text_from_file(self, filename, N):
        list_lines = []
        with open(filename) as file:
            for line in (file.readlines()[-N:]):
                print(line, end='')
                list_lines.append(line.replace("\n", ""))

        return list_lines


    def text_to_array(self, list_text):
        list_text_array = []
        for i in list_text:
            list_temp = i.split(",")
            list_text_array.append(list_temp)
        print(type(list_text_array))
        print(type(list_text_array[0]))
        print(list_text_array)
        return list_text_array
