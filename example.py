import time
import schedule
from multiprocessing import Process, Queue, Pool, Manager


def funct1(q):
    i = 0
    while True :
        print ("Number {}".format(i))
        i = i+1
        data = i
        q.put(data)
        time.sleep(10)
        print ("Done from funct1 {}".format(i))

def funct2(q):
    pool = Pool(2)
    for i in (1,2):
        data = q.get()
        #data1 = q.get()
        print ("----- Data from funct2 ---- {}".format(data))
        #print ("Data_bis from funct2 {}".format(data1))

def launch_fct2(q):
    schedule.every(30).seconds.do(funct2,q)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    manager = Manager()
    q = manager.Queue()
    
    process_one = Process(target=funct1, args= (q,))
    #process_three = mp.Process(target=launch_fct2, args = (q,))
    process_one.start()
    pool.map(launch_fct2, (q,))
    #process_two.start()
    #process_three.start()
    process_one.join()
    #process_two.join()
    #process_three.jion()