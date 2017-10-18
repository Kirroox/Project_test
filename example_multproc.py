import time
import schedule
import json
from multiprocessing import Process, Queue
from threading import RLock
import random


verrou = RLock()
data = {}
data["analyses"]={}

def creator(q):
    data = adding_data()
    print('Creating data and putting it on the queue')
    for item in data:
        print ("new status {}".format(item))
        q.put(item)
        data[item] = "INPROGRESS"

def launch_creator(q):
    schedule.every(5).seconds.do(creator,q)
    while True:
        schedule.run_pending()
        time.sleep(1)

def launch_json_reading(q1,q2):
    schedule.every(12).seconds.do(json_reading,q1,q2)
    while True:
        schedule.run_pending()
        time.sleep(1)

def json_reading(q1,q2):
    with open('analyses.json', 'r+') as f:
        file = json.load(f)
        print("HOOOOOOOO")
        data = q1.get()
        print (data)
        for item in data:
            for elmt in data[item]:
                print (data[item][elmt]) 
        '''if file["analyses"][str(data)] == "INPROGRESS":
            print ("heyyyyyyyyyy")
            print ("AA : {} --- {}".format(data,file["analyses"][str(data)]))
            #print ("new anaysis TODO")
            q2.put(str(data))
            file["analyses"][str(data)] == 'CALCULATING'
            f.seek(0)
            json.dump(file,f,indent=4)
            f.truncate()'''

def adding_in_json(q):
    with open('analyses.json', 'r+') as f:
        file = json.load(f)
        print ("adding json")
        #for item in range(100,200):
        #print ("wait")
        #time.sleep(5)
        #q.put(item)
        file["analyses"]["RefID"] = "1"
        file["analyses"]["workflows"]["step1"] = "Prescreening"
        file["analyses"]["workflows"]["step2"] = "Preprocessing"
        file["analyses"]["workflows"]["step3"] = "Taxonomy"
        analysis = file
        q.put(analysis)
        f.seek(0)
        json.dump(file,f,indent=4)
        f.truncate()
        print("new analisis")  

def launch_adding_in_json(q):
    schedule.every(5).seconds.do(adding_in_json,q)
    while True:
        schedule.run_pending()
        time.sleep(1)

def adding_data():
    data = {}
    i = 1
    while i < 10:
        data[i]="ToDo"
        i = i + 1
    return (data)

def my_consumer(q2):
    while True:
        data = q2.get()
        print('data found to be processed: {}'.format(data))
        processed = data * 2
        print(processed)

if __name__ == '__main__':
    q1 = Queue()
    q2 = Queue()
    process_one = Process(target=adding_in_json,args=(q1,))
    process_two = Process(target=launch_json_reading, args=(q1,q2))
    process_three = Process(target=my_consumer, args=(q2,))
    process_one.start()
    process_two.start()
    process_three.start()
 
    q1.close()
    q2.close()
    q1.join_thread()
    q2.join_thread()
 
    process_one.join()
    process_two.join()
    process_three.join()