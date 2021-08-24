from multiprocessing import Process, Queue
import random

def rand_num(arg1):
    print(arg1)
    num = random.random()
    print(num)

if __name__ == "__main__":
    queue = Queue()
    list = ["ARGUMENT1"]
    processes = [Process(target=rand_num, args=(list)) for x in range(5)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()