import logging
from kiteconnect import KiteTicker
import csv
import timeit
from datetime import *
import os

logging.basicConfig(level=logging.DEBUG)

#https://kite.trade/connect/login?api_key=rcpm0qsa3tuuflu5&v=3


# Initialise
kws = KiteTicker("rcpm0qsa3tuuflu5", "YFhb0wEEBMTw0wqNteteZ04honcxoUJK")

# Python program to illustrate the concept
# of threading
# importing the threading module
import threading


def print_cube(num):
    """
    function to print cube of given num
    """
    print("Cube: {}".format(num * num * num))


def print_square(num):
    """
    function to print square of given num
    """
    print("Square: {}".format(num * num))

def execute_file(file_name, index, scrip):
    """
    function to print square of given num
    """
    print("File_name from mt file:" + str(file_name))
    print("Index from mt file :" + str(index))

    # from subprocess import call
    # call(["python", "main_mt1.py"])

    import os
    print("Passing Parameters: python main_mt1.py " + str(index) + " " + str(scrip))
    os.system("python main_mt1.py " + str(index) + " " + str(scrip))


if __name__ == "__main__":
    # creating thread

    scrip = [15676930,15677186,15720450,15720706,15721730,15722242,15723010,15723522,15726850,15729154,15730690,15735810,15737090,15777282,15784194,15785474,15787522,15789570,15790338,15790594,15793410]


    # for x in range(0,36):
    #     thread = threading.Thread(target=execute_file, args=("main_mt1.py", str(x), scrip[x]))
    #     thread.start()
    #     thread.join()
    # t2 = threading.Thread(target=execute_file, args=("main_mt1.py", str(1), scrip[1]))
    # t2 = threading.Thread(target=execute_file, args=("main_mt1.py", str(0), scrip[0]))
    # t3 = threading.Thread(target=execute_file, args=("main_mt1.py", str(1), scrip[1]))
    # t4 = threading.Thread(target=execute_file, args=("main_mt1.py", str(0), scrip[0]))
    # t5 = threading.Thread(target=execute_file, args=("main_mt1.py", str(1), scrip[1]))
    # t6 = threading.Thread(target=execute_file, args=("main_mt1.py", str(0), scrip[0]))
    # t7 = threading.Thread(target=execute_file, args=("main_mt1.py", str(1), scrip[1]))
    # t8 = threading.Thread(target=execute_file, args=("main_mt1.py", str(0), scrip[0]))
    # t9 = threading.Thread(target=execute_file, args=("main_mt1.py", str(1), scrip[1]))
    thread_list = []
    for x in range(0, len(scrip)):
        thread = threading.Thread(target=execute_file, args=("main_mt1.py", str(x), scrip[x]))
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()


    # t1.start()
    # t2.start()


    # t1.join()
    # t2.join()

    # both threads completely executed
    print("Done!")
