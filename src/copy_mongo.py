#!/usr/bin/env python3
# coding: utf-8
import numpy as np
import pandas as pd
from pandas import DataFrame
import os, time
from datetime import datetime
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pymongo
import csv


import time
import os
import matplotlib.pyplot as plt
import argparse
import threading

import os, sys
from enum import IntEnum, Enum
from pymongo import MongoClient
import  bson, time , threading
# --------------------------------------------------------------Gilbert_End
settings = {
    "ip": 'localhost',  # ip:127.0.0.1
    "port": 27017,  # port
    "db_name": "rust1",  # database-name
    "set_name": "rust1_doc"  # collection-name
}
# Mongo Connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[settings["db_name"]]
mycol = mydb[settings["set_name"]]

def add_x_hours(oldtime, hr = 0 ):
    struct = time.strptime(str(oldtime), "%Y-%m-%d %H:%M:%S")
    mk = time.mktime(struct)
    real_mk = time.localtime(mk+hr*60*60)
    real_time = time.strftime("%Y-%m-%d %H:%M:%S", real_mk)
    return real_time

def time_number(oldtime):
    struct = time.strptime(str(oldtime), "%Y-%m-%d %H:%M:%S")
    mk = time.mktime(struct)
    return mk

count = 0
count2 = 0
s = 0
ab_time = []
global old_timetag,count1
count1 = 0
old_timetag = int(datetime.utcnow().timestamp() * 1000) - 1000

if __name__ == '__main__':
    db_count = 3000
    initial_leng = 3620 #902
    bottom_end = 4500#3003
    while True:
        now_timetag = int(datetime.utcnow().timestamp() * 1000) - 1000
        # Get data
        #last_update = ""
        # if (now_timetag> old_timetag and count1 < 2000 ):
        last_update = mycol.find_one({}, {'_id':0 , 'tm':1 , 'XY8002PI':1 , 'TB8002PIB':1 , 'TB8004PI':1 , 'MX8004PIB':1}, sort=[('tm', pymongo.DESCENDING)])
        # old_timetag = int(datetime.utcnow().timestamp() * 1000)
        end_duration = last_update['tm']
        end_duration_struct = time.strptime(end_duration.__str__(), "%Y-%m-%d %H:%M:%S")
        end_duration_mk = time.mktime(end_duration_struct)
        begin_duration_mk = time.localtime(end_duration_mk - 240)
        tm_year = begin_duration_mk.tm_year
        tm_mon = begin_duration_mk.tm_mon
        tm_mday = begin_duration_mk.tm_mday
        tm_hour = begin_duration_mk.tm_hour
        tm_min = begin_duration_mk.tm_min
        tm_sec = begin_duration_mk.tm_sec

        if (now_timetag> old_timetag):
            print(count1," : ", last_update , " : ", datetime.now())

            print("--------------: ",end_duration_struct, " <> ",  begin_duration_mk)
            old_timetag = int(datetime.utcnow().timestamp() * 1000)
            count1+=1
            # initial_leng =  1472 #902
            # bottom_end = 4103#3003
            if( count1 >= (bottom_end - initial_leng)):
                break
        # print(last_update)
        # end_duration = last_update['tm']
        # end_duration_struct = time.strptime(end_duration.__str__(), "%Y-%m-%d %H:%M:%S")
        # end_duration_mk = time.mktime(end_duration_struct)
        # begin_duration_mk = time.localtime(end_duration_mk - 240)
        # print("--------------: ",end_duration_struct, " <> ",  begin_duration_mk)
        # tm_year = begin_duration_mk.tm_year
        # tm_mon = begin_duration_mk.tm_mon
        # tm_mday = begin_duration_mk.tm_mday
        # tm_hour = begin_duration_mk.tm_hour
        # tm_min = begin_duration_mk.tm_min
        # tm_sec = begin_duration_mk.tm_sec
        # begin_duration = time.strftime("%Y-%m-%d %H:%M:%S", begin_duration_mk)
        # print('Begin Time:\t', begin_duration)
        # print('End Time:\t', end_duration)

        # print(mycol.count_documents({"tm":{"$gte": begin_duration}}))
        # print(mycol.count_documents({"tm":{"$gt": datetime(tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec)}}))
        cursor = mycol.find({"tm":{"$gt": datetime(tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec)}})
        data = [i for i in cursor]
        # print(len(data))

        TIME = []
        dataD = []
        dataE = []
        dataF = []
        dataG = []
        for dic in data:
            TIME.append(dic['tm'])
            dataD.append(dic['XY8002PI'])
            dataE.append(dic['TB8002PIB'])
            dataF.append(dic['TB8004PI'])
            dataG.append(dic['MX8004PIB'])

        df = DataFrame(TIME, columns=['TIME'])
        df['XY8002PI'] = dataD
        df['TB8002PIB'] = dataE
        df['TB8004PI'] = dataF
        df['MX8004PIB'] = dataG
        # print(df)

        ave_D = []
        ave_E = []
        ave_F = []
        ave_G = []
        delta_D = []
        delta_E = []
        delta_F = []
        delta_G = []

        averagescale = 30

        for i in range(df.shape[0]//averagescale):
            x = np.mean(dataD[i*averagescale:(i+1)*averagescale])
            y = np.mean(dataE[i*averagescale:(i+1)*averagescale])
            z = np.mean(dataF[i*averagescale:(i+1)*averagescale])
            w = np.mean(dataG[i*averagescale:(i+1)*averagescale])
            ave_D.append(x)
            ave_E.append(y)
            ave_F.append(z)
            ave_G.append(w)
        ave_D = np.array(ave_D)
        ave_E = np.array(ave_E)
        ave_F = np.array(ave_F)
        ave_G = np.array(ave_G)
        # print(ave_D)

        delta_D = ave_D[1:] - ave_D[:-1]
        delta_E = ave_E[1:] - ave_E[:-1]
        delta_F = ave_F[1:] - ave_F[:-1]
        delta_G = ave_G[1:] - ave_G[:-1]
        delta_D = -(np.array(delta_D))
        delta_E = -(np.array(delta_E))
        delta_F = -(np.array(delta_F))
        delta_G = -(np.array(delta_G))
        # print(delta_D_scale)

        # peaks1, _ = find_peaks(ave_D, height=0.01, distance = 500, width=1)
        # peaks2, _ = find_peaks(timewindow_E, height=0.01, distance = 500, width=1)
        # peaks3, _ = find_peaks(timewindow_F, height=0.01, distance = 500, width=1)
        # peaks4, _ = find_peaks(timewindow_G, height=0.01, distance = 500, width=1)
        peaks9 , _ = find_peaks(delta_D, height=0.03,width=1.5)
        peaks10, _ = find_peaks(delta_E, height=0.03,width=1.5)
        peaks11, _ = find_peaks(delta_F, height=0.03,width=1.5)
        peaks12, _ = find_peaks(delta_G, height=0.03,width=1.5)

        # fig,axes = plt.subplots(4, 2, figsize=(10,7) )
        # axes[0,0].plot(ave_D)
        # # axes[0,0].plot(peaks1, ave_D[peaks1],"xr")
        # axes[0,0].set_title('XY8002PI', fontsize=7)
        # axes[1,0].plot(ave_E)
        # # axes[1,0].plot(peaks2, ave_E[peaks2],"xr")
        # axes[1,0].set_title('TB8002PIB', fontsize=7)
        # axes[2,0].plot(ave_F)
        # # axes[2,0].plot(peaks3, ave_F[peaks3],"xr")
        # axes[2,0].set_title('TB8004PI', fontsize=7)
        # axes[3,0].plot(ave_G)
        # # axes[3,0].plot(peaks4, ave_G[peaks4],"xr")
        # axes[3,0].set_title('MX8004PIB', fontsize=7)

        # axes[0,1].plot(delta_D)
        # axes[0,1].plot(peaks9, delta_D[peaks9],"xr")
        # axes[0,1].set_title('Δ TB8004PI', fontsize=7)
        # axes[1,1].plot(delta_E)
        # axes[1,1].plot(peaks10, delta_E[peaks10],"xr")
        # axes[1,1].set_title('Δ MX8004PIB', fontsize=7)
        # axes[2,1].plot(delta_F)
        # axes[2,1].plot(peaks11, delta_F[peaks11],"xr")
        # axes[2,1].set_title('Δ TB8004PI', fontsize=7)
        # axes[3,1].plot(delta_G)
        # axes[3,1].plot(peaks12, delta_G[peaks12],"xr")
        # axes[3,1].set_title('Δ MX8004PIB', fontsize=7)

        # plt.savefig("look.png")
        #plt.show()

        compare1 = list(peaks9)+list(peaks10)
        compare2 = list(peaks11)+list(peaks12)
        compare1.sort()
        compare2.sort()
        getpeak1 = []
        getpeak2 = []

        for i in range(len(compare1)-1):
            if abs(compare1[i]-compare1[i+1])<2:
                getpeak1.append(compare1[i])
        getpeaktime1 = np.array(getpeak1)*averagescale

        for i in range(len(compare2)-1):
            if abs(compare2[i]-compare2[i+1])<2 :
                getpeak2.append(compare2[i])
        getpeaktime2 = np.array(getpeak2)*averagescale

        time_l = []
        if getpeaktime1.shape[0] <= 0 and getpeaktime2.shape[0] <= 0:
            count = count+1
            count2 = 0
            if count == db_count:
                count = 0
                try:
                    real_time = add_x_hours(df.iloc[239,0])

                    print('=== normal === '+str(real_time))
                    with open('now.csv','w') as f:
                        writer = csv.writer(f)
                        t = []
                        t.append(real_time)
                        writer.writerow(t)

                    # f = open("abnormal_time.txt",'a')
                    # f.write('=== abnormal ==='+'\n')
                    # f.close

                except:
                    #print("can't Connect mongo")
                    pass

            # print('=== normal ===')

        else:
            count2 = count2+1
            # print('=== abnormal ===')
            if count2 == 1:
                count2 = 0
                # s = s + 1
                # df.to_csv(str(s)+'error.csv', index=False)
                for i in getpeaktime1:
                    time_l.append(add_x_hours(df.iloc[i, 0])+" 8002 pipeline")
                    ab_time.append(time_number(df.iloc[i, 0]))
                for i in getpeaktime2:
                    time_l.append(add_x_hours(df.iloc[i, 0])+" 8004 pipeline")
                    ab_time.append(time_number(df.iloc[i, 0]))
                time_l.sort()

                # ab_time.append(time_number(df.iloc[i, 0]))
                if ab_time[len(ab_time)-1]>(30+ab_time[len(ab_time)-2]) or len(ab_time)==1:


                    # print(ab_time[len(ab_time)-1])
                    # print(len(ab_time))
                    # print(time_l)

                    for i in time_l:
                        print('=== abnormal === '+str(i))
                        f = open('abnormal_time.txt','a')
                        f.write('=== abnormal === '+i+'\n')
                        f.close

                        with open('abnormal.csv','w') as file:
                            writer = csv.writer(file)
                            ti = []
                            ti.append(i)
                            writer.writerow(ti)



        """
        import numpy as np
import pandas as pd
from pandas import DataFrame
import os, time
from datetime import datetime
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pymongo
import csv

# Mongo Connection
myclient = pymongo.MongoClient("mongodb://192.168.100.8:27017/")
mycol = myclient.RTTM.MergeData

def add_8_hours(oldtime):
    struct = time.strptime(str(oldtime), "%Y-%m-%d %H:%M:%S")
    mk = time.mktime(struct)
    real_mk = time.localtime(mk+8*60*60)
    real_time = time.strftime("%Y-%m-%d %H:%M:%S", real_mk)
    return real_time

def time_number(oldtime):
    struct = time.strptime(str(oldtime), "%Y-%m-%d %H:%M:%S")
    mk = time.mktime(struct)
    return mk

count = 0
count2 = 0
s = 0
ab_time = []
if __name__ == '__main__':

    while True:
        # Get data
        last_update = mycol.find_one({}, {'_id':0 , 'tm':1 , 'XY8002PI':1 , 'TB8002PIB':1 , 'TB8004PI':1 , 'MX8004PIB':1}, sort=[('tm', pymongo.DESCENDING)])
        # print(last_update)
        end_duration = last_update['tm']
        end_duration_struct = time.strptime(str(end_duration), "%Y-%m-%d %H:%M:%S")
        end_duration_mk = time.mktime(end_duration_struct)
        begin_duration_mk = time.localtime(end_duration_mk-240)
        tm_year = begin_duration_mk.tm_year
        tm_mon = begin_duration_mk.tm_mon
        tm_mday = begin_duration_mk.tm_mday
        tm_hour = begin_duration_mk.tm_hour
        tm_min = begin_duration_mk.tm_min
        tm_sec = begin_duration_mk.tm_sec
        # begin_duration = time.strftime("%Y-%m-%d %H:%M:%S", begin_duration_mk)
        # print('Begin Time:\t', begin_duration)
        # print('End Time:\t', end_duration)

        # print(mycol.count_documents({"tm":{"$gte": begin_duration}}))
        # print(mycol.count_documents({"tm":{"$gt": datetime(tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec)}}))
        cursor = mycol.find({"tm":{"$gt": datetime(tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec)}})
        data = [i for i in cursor]
        # print(len(data))

        TIME = []
        dataD = []
        dataE = []
        dataF = []
        dataG = []
        for dic in data:
            TIME.append(dic['tm'])
            dataD.append(dic['XY8002PI'])
            dataE.append(dic['TB8002PIB'])
            dataF.append(dic['TB8004PI'])
            dataG.append(dic['MX8004PIB'])

        df = DataFrame(TIME, columns=['TIME'])
        df['XY8002PI'] = rawdf['XY8002PI']
        df['TB8002PIB'] = rawdf['TB8002PIB']
        df['TB8004PI'] = rawdf['TB8004PI']
        df['MX8004PIB'] = rawdf['MX8004PIB']
        # print(df)

        ave_D = []
        ave_E = []
        ave_F = []
        ave_G = []
        delta_D = []
        delta_E = []
        delta_F = []
        delta_G = []

        averagescale = 30

        for i in range(df.shape[0]//averagescale):
            x = np.mean(dataD[i*averagescale:(i+1)*averagescale])
            y = np.mean(dataE[i*averagescale:(i+1)*averagescale])
            z = np.mean(dataF[i*averagescale:(i+1)*averagescale])
            w = np.mean(dataG[i*averagescale:(i+1)*averagescale])
            ave_D.append(x)
            ave_E.append(y)
            ave_F.append(z)
            ave_G.append(w)
        ave_D = np.array(ave_D)
        ave_E = np.array(ave_E)
        ave_F = np.array(ave_F)
        ave_G = np.array(ave_G)
        # print(ave_D)

        delta_D = ave_D[1:] - ave_D[:-1]
        delta_E = ave_E[1:] - ave_E[:-1]
        delta_F = ave_F[1:] - ave_F[:-1]
        delta_G = ave_G[1:] - ave_G[:-1]
        delta_D = -(np.array(delta_D))
        delta_E = -(np.array(delta_E))
        delta_F = -(np.array(delta_F))
        delta_G = -(np.array(delta_G))
        # print(delta_D_scale)

        # peaks1, _ = find_peaks(ave_D, height=0.01, distance = 500, width=1)
        # peaks2, _ = find_peaks(timewindow_E, height=0.01, distance = 500, width=1)
        # peaks3, _ = find_peaks(timewindow_F, height=0.01, distance = 500, width=1)
        # peaks4, _ = find_peaks(timewindow_G, height=0.01, distance = 500, width=1)
        peaks9 , _ = find_peaks(delta_D, height=0.03,width=1.5)
        peaks10, _ = find_peaks(delta_E, height=0.03,width=1.5)
        peaks11, _ = find_peaks(delta_F, height=0.03,width=1.5)
        peaks12, _ = find_peaks(delta_G, height=0.03,width=1.5)

        # fig,axes = plt.subplots(4, 2, figsize=(10,7) )
        # axes[0,0].plot(ave_D)
        # # axes[0,0].plot(peaks1, ave_D[peaks1],"xr")
        # axes[0,0].set_title('XY8002PI', fontsize=7)
        # axes[1,0].plot(ave_E)
        # # axes[1,0].plot(peaks2, ave_E[peaks2],"xr")
        # axes[1,0].set_title('TB8002PIB', fontsize=7)
        # axes[2,0].plot(ave_F)
        # # axes[2,0].plot(peaks3, ave_F[peaks3],"xr")
        # axes[2,0].set_title('TB8004PI', fontsize=7)
        # axes[3,0].plot(ave_G)
        # # axes[3,0].plot(peaks4, ave_G[peaks4],"xr")
        # axes[3,0].set_title('MX8004PIB', fontsize=7)

        # axes[0,1].plot(delta_D)
        # axes[0,1].plot(peaks9, delta_D[peaks9],"xr")
        # axes[0,1].set_title('Δ TB8004PI', fontsize=7)
        # axes[1,1].plot(delta_E)
        # axes[1,1].plot(peaks10, delta_E[peaks10],"xr")
        # axes[1,1].set_title('Δ MX8004PIB', fontsize=7)
        # axes[2,1].plot(delta_F)
        # axes[2,1].plot(peaks11, delta_F[peaks11],"xr")
        # axes[2,1].set_title('Δ TB8004PI', fontsize=7)
        # axes[3,1].plot(delta_G)
        # axes[3,1].plot(peaks12, delta_G[peaks12],"xr")
        # axes[3,1].set_title('Δ MX8004PIB', fontsize=7)

        # plt.savefig("look.png")
        #plt.show()

        compare1 = list(peaks9)+list(peaks10)
        compare2 = list(peaks11)+list(peaks12)
        # print("1",compare1)
        compare1.sort()
        compare2.sort()
        # print("2",compare1)
        getpeak1 = []
        getpeak2 = []

        for i in range(len(compare1)-1):
            if abs(compare1[i]-compare1[i+1])<2:
                getpeak1.append(compare1[i])
        getpeaktime1 = np.array(getpeak1)*averagescale

        for i in range(len(compare2)-1):
            if abs(compare2[i]-compare2[i+1])<2 :
                getpeak2.append(compare2[i])
        getpeaktime2 = np.array(getpeak2)*averagescale

        time_l = []
        if getpeaktime1.shape[0] <= 0 and getpeaktime2.shape[0] <= 0:
            count = count+1
            count2 = 0
            if count == 3000:
                count = 0
                try:
                    real_time = add_8_hours(df.iloc[239,0])

                    print('=== normal === '+str(real_time))
                    with open('now.csv','w') as f:
                        writer = csv.writer(f)
                        t = []
                        t.append(real_time)
                        writer.writerow(t)

                    # f = open("abnormal_time.txt",'a')
                    # f.write('=== abnormal ==='+'\n')
                    # f.close

                except:
                    print("can't Connect mongo")

            # print('=== normal ===')

        else: #getpeaktime1.shape[0] <= 0 and getpeaktime2.shape[0] <= 0:
            count2 = count2+1
            # print('=== abnormal ===')
            if count2 == 1:
                count2 = 0
                # s = s + 1
                # df.to_csv(str(s)+'error.csv', index=False)
                for i in getpeaktime1:
                    time_l.append(add_8_hours(df.iloc[i, 0])+" 8002 pipeline")
                    ab_time.append(time_number(df.iloc[i, 0]))
                for i in getpeaktime2:
                    time_l.append(add_8_hours(df.iloc[i, 0])+" 8004 pipeline")
                    ab_time.append(time_number(df.iloc[i, 0]))
                time_l.sort()

                # ab_time.append(time_number(df.iloc[i, 0]))
                if ab_time[len(ab_time)-1]>(30+ab_time[len(ab_time)-2]) or len(ab_time)==1:


                    # print(ab_time[len(ab_time)-1])
                    # print(len(ab_time))
                    # print(time_l)

                    for i in time_l:
                        print('=== abnormal === '+str(i))
                        f = open('abnormal_time.txt','a')
                        f.write('=== abnormal === '+i+'\n')
                        f.close

                        with open('abnormal.csv','w') as file:
                            writer = csv.writer(file)
                            ti = []
                            ti.append(i)
                            writer.writerow(ti)

        
        
        === abnormal === 2021-06-30 19:00:02 8002 pipeline
        === abnormal === 2021-06-30 19:02:03 8002 pipeline
        === abnormal === 2021-06-30 19:09:57 8002 pipeline
        === abnormal === 2021-06-30 19:11:45 8002 pipeline
        === abnormal === 2021-06-30 19:17:00 8002 pipeline
        """