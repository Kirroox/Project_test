import time
import multiprocessing as mp


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
    while True:
        data = q.get()
        print (data)
        time.sleep(30)
        print ("Done from funct2 {}".format(data))


if __name__ == '__main__':
    q = mp.Queue()

    process_one = mp.Process(target=funct1, args= (q,))
    process_two = mp.Process(target=funct2, args = (q,))

    process_one.start()
    process_two.start()

    process_one.join()
    process_two.join()
