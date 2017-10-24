import time
import sys
import os
import schedule
from multiprocessing import Process, Queue, Pool, Manager

def funct1(q):
    try:
        i = 0
        while True :
            print ("Number {}".format(i))
            i = i+1
            data = i
            q.put(data)
            time.sleep(10)
            print ("Done from funct1 {}".format(i))
    except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

def print_fct(elmt):
    time.sleep(10)
    print ("----- Data from funct2 ---- {}".format(elmt))

def funct2(q):
    try:
        data = []
        pool = Pool(2)
        for i in (1,2):
            cc = q.get()
            data.append(cc)
        pool.map(print_fct, data)
        pool.close()
    except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

def launch_fct2(q):
    try:
        schedule.every(30).seconds.do(funct2,q)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
            
if __name__ == '__main__':
    try:
        q = Queue()
    
        process_one = Process(target=funct1, args= (q,))
        process_two = Process(target=launch_fct2, args= (q,))

        process_one.start()
        process_two.start()

        q.close()
        q.join_thread()
        process_one.join()
        process_two.join()
    except KeyboardInterrupt:
        print ('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)