# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 15:26:15 2020

@author: Hemu
"""

import time
import socket 
import sys
import json
import random
import threading
import copy

def mod(task_bag):
  if task_bag!="":

    t = json.loads(task_bag)
    jt_pool[t['task_id']]=t
    jt_pool[t['task_id']]['start_time']=time.time()
  return jt_pool

def con_ect(eaves_drop):
  link,hostad = eaves_drop.accept()
  task = link.recv(1024)
  ele = task.decode()
  task_bag = ""
  while task:
    task_bag = task_bag + ele
    task = link.recv(1024)
  mod(task_bag)
  link.close()
  



def bag_of_tasks(eaves_drop):
    eaves_drop.listen(1)
    while True:
        task = con_ect(eaves_drop)

def mimic(worker_id,host,port):
  print("inside mimic")
  while True:
    i = 0
    while(len(jt_pool)>0 and (i==0)):
    #if len(jt_pool)>0:
      i = i+1
      t = copy.deepcopy(jt_pool)
      for task_id in t:
        jt_pool[task_id]['duration'] -= 1
        print("current time for task",task_id,":",time.time())
        i1 = 0
        #while((jt_pool[task_id]['duration'] == 0) and (i1==0)):
        if jt_pool[task_id]['duration'] == 0:
          #i1 = i1+1
          print("Updated task ")
          print("Task finished in worker :",task_id)
          jt_pool[task_id]['end_time'] = time.time()
          mimic_s = socket.socket()
          mimic_s.connect((host,port))
          jt_pool[task_id]['w_id'] = worker_id
          mimic_s.send(json.dumps(jt_pool[task_id]).encode())
          mimic_s.close()
          del jt_pool[task_id]

if __name__ == '__main__':
  eaves_drop=socket.socket()
  host = 'localhost'
  port = int(sys.argv[1])
  worker_id = int(sys.argv[2])

  eaves_dropet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  eaves_dropet.bind((host,port))   
  jt_pool={}
  #After obtaining the worker_id and port we will call the addtask function using threads
  t4=threading.Thread(target=bag_of_tasks, name = "Thread4", args=(eaves_dropet,))
  t4.start()

  t5=threading.Thread(target=mimic, name = "Thread5", args=(worker_id,"localhost",5001,))
  t5.start()

  t4.join()
  t5.join()
