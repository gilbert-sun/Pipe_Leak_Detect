#!/usr/bin/env python3
# coding: utf-8
import numpy as np
from pandas import DataFrame
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
import os, datetime

yourpath = '/home/gilbert3/Downloads/leak數據/'
all_file_list = os.listdir(yourpath)
all_file_list = sorted(all_file_list)
filename = 0
file = yourpath + all_file_list[filename]
print(all_file_list[filename])
dataframe = pd.read_csv(file)

dataA = dataframe['時間']
# dataD = dataframe['XY8002PI']
# dataE = dataframe['TB8002PIB']
# dataF = dataframe['TB8004PI']
# dataG = dataframe['MX8004PIB']
dataD = dataframe['新營壓力']
dataE = dataframe['太保壓力北']
dataF = dataframe['太保壓力南']
dataG = dataframe['民雄壓力']
"""
db.rust1_doc.insert({
    tm:     "2021-11-29T11:12:02.256Z", 
    f2PI:   0.01,
    f2PIB:  0.02,
    f4PI:   0.03,
    f4PIB:  0.04
})
"""
# --------------------------------------------------------------Begin
settings = {
    "ip": 'localhost',      # ip:127.0.0.1
    "port": 27017,          # port
    "db_name": "rust1",     # database-name
    "set_name": "rust1_doc" # collection-name
}

class MongoLogDBmodel(object):
    tm = ""
    XY8002PI = ""
    TB8002PIB = ""
    TB8004PI = ""
    MX8004PIB = ""

    def __init__(self,tm, v1, v2, v3 , v4 ):

        self.tm = datetime.datetime.strptime(tm, "%Y-%m-%d %H:%M:%S")
        self.XY8002PI = v1
        self.TB8002PIB = v2
        self.TB8004PI = v3
        self.MX8004PIB = v4

    def set(self, tm,v1, v2, v3 , v4):
        # self.Datetimetag = bson.Int64(int(datetime.datetime.utcnow().timestamp() * 1000))
        # self.Timestamp = datetime.datetime.strptime("2021-11-30 22:23:38", "%Y-%m-%d %H:%M:%S") #datetime.datetime.utcnow()
        self.tm = datetime.datetime.strptime(tm, "%Y-%m-%d %H:%M:%S")
        self.XY8002PI = v1
        self.TB8002PIB = v2
        self.TB8004PI = v3
        self.MX8004PIB = v4

    def get(self):
        return self.__dict__


class RustLogModelServices(object):
    def __init__(self):
        try:
            self.conn = MongoClient(settings["ip"], settings["port"])
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.my_set = self.db[settings["set_name"]]

    # mongoDB c-r-u-d
    def create(self, model_dic):
        print("insert...1")
        self.my_set.insert_one(model_dic)

    def createdb(self, tm, f2PI, f2PIB, f4PI, f4PIB ):
        print("insert...2")
        log = MongoLogDBmodel(tm, f2PI,f2PIB,f4PI,f4PIB)
        self.my_set.insert_one(log.get())

    def update(self, model_dic, newdic):
        print("update...")
        self.my_set.update(model_dic, newdic)

    def delete(self, model_dic):
        print("delete...")
        self.my_set.remove(model_dic)

    def dbread(self):
        print("find...")
        data = self.my_set.find()
        for idx in range((data.count())):
            print(idx," : ",data[idx]["tm"]," : ",data[idx] ["p2PI"])

    def dbreadall(self):
        print("list all...\n")
        datas = self.my_set.find()
        for idx in range(datas.count()):
            print("\n[{}]----------------------------------------------".format(idx) )
            for k,v in datas[idx].items():
                print(k," : ",v)


def async_wrDB1():
    global old_timetag,mongo,count
    now_timetag = int(datetime.datetime.utcnow().timestamp() * 1000) - 1000
    # initial_leng =  1472 #902
    # bottom_end = 4103#3003
    leng = len(dataD[initial_leng:bottom_end])
    if now_timetag> old_timetag and  count < leng:
        Msg = "------Alive, MongoDB connected!-------"
        # mongo.createdb("2021-11-30 23:22:11", 0.34, 0.32,0.33,0.34)
        # print("\n{} : {}\n".format(count+1 ,Msg))
        old_timetag = int(datetime.datetime.utcnow().timestamp() * 1000)
        # for idx in range(len(dataD[1167:1348])):
        mongo.createdb(dataA[initial_leng+count], dataD[initial_leng+count], dataE[initial_leng+count],dataF[initial_leng+count],dataG[initial_leng+count])
        print(count," : ", datetime.datetime.now(),dataA[initial_leng+count]," : ",dataD[initial_leng+count])
        count += 1


def run():
    global mongo, old_timetag
    mongo = RustLogModelServices()
    old_timetag = int(datetime.datetime.utcnow().timestamp() * 1000)
    initial_leng =  1472 #902
    bottom_end = 4103#3003
    leng = len(dataD[initial_leng:bottom_end])
    while True:
        async_wrDB1()
        if(count >= leng):
            break
    print("-------------------------Write DB End")


if __name__ == "__main__":
    global old_timetag,count, initial_leng, bottom_end
    initial_leng =  1950 #902
    bottom_end = 7600 #3003
    count = 0
    old_timetag = int(datetime.datetime.utcnow().timestamp() * 1000)
    run()