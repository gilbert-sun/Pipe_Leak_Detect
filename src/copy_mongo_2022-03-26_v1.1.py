#!/usr/bin/env python3
# coding: utf-8
import numpy as np
import pandas as pd
from pandas import DataFrame
import os, time
from datetime import datetime, timedelta
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pymongo
import csv

# Mongo Connection
myclient = pymongo.MongoClient("mongodb://192.168.1.213:27017/")
mycol = myclient.RTTM.MergeData

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
#--------------------------------------------------------------------------------------------------------------2022-03-26,gilbert_start
#--------------------------------------------------------------------------------------------------------------2022-03-26,gilbert
def compare_8002Time(NorthPeak,SouthPeak):
    struct1 = strptime((NorthPeak), "%Y-%m-%d %H:%M:%S")
    NT = mktime(struct1)
    struct2 = strptime((SouthPeak), "%Y-%m-%d %H:%M:%S")
    ST = mktime(struct2)
    #ST = 23 / NT = 41
    #ST = 23 / NT = 21
    #ST = 21 / NT = 44
    if ST - NT > 0:
        return False
    elif ST - NT > 0 and ST - NT < 5:
        return False
    elif NT - ST > 10:
        return True


def compare_2Time(NorthPeak,SouthPeak):
    struct1 = strptime((NorthPeak), "%Y-%m-%d %H:%M:%S")
    NT = mktime(struct1)
    struct2 = strptime((SouthPeak), "%Y-%m-%d %H:%M:%S")
    ST = mktime(struct2)
    #ST = 23 / NT = 21
    #ST = 20 / NT = 21
    #ST = 21 / NT = 44
    if ST - NT > 0:
        return True
    elif ST - NT < 0 and NT - ST < 5:
        return True
    elif NT - ST > 10:
        return False

def compare_NS(NorthPeak,SouthPeak):

    lastLines = SouthPeak.split()
    lastLines1 = NorthPeak.split()
    # print("----------------:Hello: ", lastLines[3].split("-"), lastLines[4].split(":"))
    # if lastLines != [] :
    STime = datetime((int)(lastLines[0].split("-")[0]), (int)(lastLines[0].split("-")[1]),
                     (int)(lastLines[0].split("-")[2]), (int)(lastLines[1].split(":")[0]),
                     (int)(lastLines[1].split(":")[1]), (int)(lastLines[1].split(":")[2]))
    #         print ("=====================33> ", fTime, type(fTime))
    NTime = datetime((int)(lastLines1[0].split("-")[0]), (int)(lastLines1[0].split("-")[1]),
                     (int)(lastLines1[0].split("-")[2]), (int)(lastLines1[1].split(":")[0]),
                     (int)(lastLines1[1].split(":")[1]), (int)(lastLines1[1].split(":")[2]))
    #ST = 33 / NT = 20
    # 33 -10 > 20
    # and
    # 33 -15  < 20
    if     (NTime ) >= STime:
        return True
    else:
        return False

def find_1match_peakTime(NorthPeak,SouthPeak):
    struct1 = strptime((NorthPeak), "%Y-%m-%d %H:%M:%S")
    NT = mktime(struct1)
    struct2 = strptime((SouthPeak), "%Y-%m-%d %H:%M:%S")
    ST = mktime(struct2)
    return ST - NT

def find_2match_peakTime(NorthPeak,SouthPeak):

    lastLines = SouthPeak.split()
    lastLines1 = NorthPeak.split()
    # print("----------------:Hello: ", lastLines[3].split("-"), lastLines[4].split(":"))
    # if lastLines != [] :
    ST = datetime((int)(lastLines[0].split("-")[0]), (int)(lastLines[0].split("-")[1]),
                  (int)(lastLines[0].split("-")[2]), (int)(lastLines[1].split(":")[0]),
                  (int)(lastLines[1].split(":")[1]), (int)(lastLines[1].split(":")[2]))
    #         print ("=====================33> ", fTime, type(fTime))
    NT = datetime((int)(lastLines1[0].split("-")[0]), (int)(lastLines1[0].split("-")[1]),
                  (int)(lastLines1[0].split("-")[2]), (int)(lastLines1[1].split(":")[0]),
                  (int)(lastLines1[1].split(":")[1]), (int)(lastLines1[1].split(":")[2]))
    #ST = 33 / NT = 20
    # 33 -10 > 20
    # and
    # 33 -15  < 20
    # if     (STime - timedelta(seconds=10)) >= NTime and (STime - timedelta(seconds=15)) <= NTime:
    #ST = 23 / NT = 21
    #ST = 20 / NT = 21
    #ST = 21 / NT = 44
    return NT - ST


def find_last_peak_and_plot_8002():
    global IDx, i, sect_all, sect_A, sect_B, idx, sect_BB, sect_AA, peak2, _, dic1, dic2, lresult1, lresult2, fResult, tmp, tmp1, sect_all1, sect_A1, sect_B1, sect_BB1, sect_AA1, peak4, dic3, dic4, lresult3, lresult4, lresult_south, tmpResult, fig, axes
    IDx = 0
    tmpIndex = 2
    print("#getpeaktime1------------------------------------------------------------------------------------------------------------")
    for i in getpeaktime1:
        print("============================================================================================================================")
        print("Ans--8002: "," <=> ",i, df.iloc[i, 0], " <=> ", (df.iloc[i, 4-tmpIndex]), ":" ,type(df.iloc[i, 5 - tmpIndex]) , ":" ,(df.iloc[i, 6 - tmpIndex]))
        print("============================================================================================================================")
        time_l.append(df.iloc[i, 0])

        IDx += 1
        p8002_1 = 30
        p8002_2 = 60
        p8002_3 = 15
        sect_all = df.iloc[i - p8002_1:i + p8002_2, 0]
        sect_A = []
        sect_B = []
        for idx in range(-p8002_1, p8002_2):
            sect_A.append(df.iloc[idx + i, 3 - tmpIndex] - df.iloc[idx + i + 1, 3 - tmpIndex])
            sect_B.append(df.iloc[idx + i, 3 - tmpIndex])
        sect_BB = (np.array(sect_B))
        sect_AA = (np.array(sect_A))

        #8002 _ North---------------------------------------------------------------------------------------------------------
        peak2, _ = find_peaks(sect_AA, height=0.001, width=0.1)
        dic1 = {}
        dic2 = {}
        lresult1 = []
        lresult2 = []
        for idx in range(-p8002_1, p8002_2):
            if (df.iloc[i + idx, 3-tmpIndex] - df.iloc[i + idx + 2, 3-tmpIndex]) > 0.001:
                print(str(idx) + "). --------------N:8002_1--------->>> ", df.iloc[i + idx, 0], " <=> ",
                      df.iloc[i + idx, 3-tmpIndex] - df.iloc[i + idx + 2, 3-tmpIndex])
                dic1[str(df.iloc[i + idx, 0])] = df.iloc[i + idx, 3-tmpIndex] - df.iloc[i + 2 + idx, 3-tmpIndex]

        for idx in range(-p8002_1, p8002_3):
            if (df.iloc[i + idx, 3-tmpIndex] - df.iloc[i + 2 + idx, 3-tmpIndex]) > 0.01:
                dic2[str(df.iloc[i + idx, 0])] = df.iloc[i + idx, 3-tmpIndex] - df.iloc[i + 2 + idx, 3-tmpIndex]

        print("-----------N:8002_2------------>>> ", i, " <=> ", peak2, " <=> ", df.iloc[i, 0]," <=> ",df.iloc[i, 3-tmpIndex])

        if (dic2 != {}):
            lresult2 = sorted(dic2.items(), key=lambda d: d[1], reverse=True)
            print("-----------N:8002_3.1------------>>> ", lresult2)  # ," <=> ", lresult2[0], " <=> ", lresult2[1])
        elif (dic1 != {}):
            lresult2 = sorted(dic1.items(), key=lambda d: d[1], reverse=True)
            print("-----------N:8002_3.2------------>>> ", lresult2)  # ," <=> ", lresult2[0], " <=> ", lresult2[1])
        if len(lresult2) > 1:
            fResult = compare_8002Time(lresult2[0][0], lresult2[1][0])
        else:
            fResult = False

        if fResult == True:
            tmp = lresult2[0]
            tmp1 = lresult2[1]
            lresult2[0] = tmp1
            lresult2[1] = tmp

        if (dic1 != {} and fResult == True):

            lresult1 = sorted(dic1.items(), key=lambda d: d[1], reverse=True)
            lresult2 = sorted(dic2.items(), key=lambda d: d[1], reverse=True)
            print("-----------N:8002_4_1, lresult1 = ------------>>> ", lresult1)#-30 ~60
            print("-----------N:8002_4_1.1, lresult2 = ------------>>> ", lresult2)# -30 ~ 15
            print("-----------N:8002_4_1.1, fResult = ------------>>> ", fResult)
        else:
            print("-----------N:8002_4_2, lresult2 = ------------>>> ", lresult2)
            print("-----------N:8002_4_2.1,fResult = ------------>>> ", fResult)

        print("============---N:8002_5-------lresult12----------->> ", lresult2)

        if (len(peak2) > 0):
            print("-----------N:8002_6.1---------peak2--->>> ", df.iloc[i + peak2[0], 0]," : ",peak2)
        else:
            print("-----------N:8002_6_2------------>>> ", i, peak2)

        # 8002 _ South---------------------------------------------------------------------------------------

        sect_all1 = df.iloc[i - p8002_1:i + p8002_2, 0]
        sect_A1 = []
        sect_B1 = []
        for idx in range(-p8002_1, p8002_2):
            sect_A1.append(df.iloc[idx + i, 4 - tmpIndex] - df.iloc[idx + i + 1, 4- tmpIndex])
            sect_B1.append(df.iloc[idx + i, 4 - tmpIndex])
        sect_BB1 = (np.array(sect_B1))
        sect_AA1 = (np.array(sect_A1))

        peak4, _ = find_peaks(sect_AA1, height=0.001, width=0.1)
        dic3 = {}
        dic4 = {}
        lresult3 = []
        lresult4 = []

        for idx in range(-p8002_1, p8002_2):
            if (df.iloc[i + idx, 4- tmpIndex] - df.iloc[i + 2 + idx, 4- tmpIndex]) > 0.005:
                print(str(idx) + "). --------------S:8002_7--------->>> ", df.iloc[i + idx, 0], " <=> ",
                      df.iloc[i + idx, 4- tmpIndex] - df.iloc[i + 2 + idx, 4- tmpIndex])
                dic3[str(df.iloc[i + idx, 0])] = df.iloc[i + idx, 4- tmpIndex] - df.iloc[i + 2 + idx, 4- tmpIndex]

        for idx in range(-p8002_1, p8002_3):
            if (df.iloc[i + idx, 4 - tmpIndex] - df.iloc[i + 2 + idx, 4 - tmpIndex]) > 0.01:
                dic4[str(df.iloc[i + idx, 0])] = df.iloc[i + idx, 4 - tmpIndex] - df.iloc[i + 2 + idx, 4 - tmpIndex]

        lresult3 = sorted(dic3.items(), key=lambda d: d[1], reverse=True)
        print("============----------S:8002_8  ------ lresult3:----------->> ", lresult3)

        lresult_south = []
        # find south - north >= 10 && <=12 , south =32 later, north = 22
        if lresult2 != []:
            for idx in range(len(lresult3)):
                tmpResult = find_1match_peakTime(lresult2[0][0], lresult3[idx][0])
                print("S:8002_9============!!!>> ", lresult3[idx][0], " <=> ", lresult3[idx][1], " <=> ", tmpResult)
                if tmpResult <= -10 and tmpResult >= -25:
                    print(">>>>>>>>>>>>>>>>>>>>>>>>> --------S:8002_10 : Got it South_0!--------  >>>>>>>>>>>>>>>>>>>> ", lresult3[idx])
                    lresult_south.append(lresult3[idx])

        print("-----------S:8002_11------------>>> ", i, " <=> ", peak4, " <=> ", df.iloc[i, 0] ," <=> ",df.iloc[i, 4 - tmpIndex] )

        if (dic4 != {}):
            print("-----------S:8002_12.1------------>>> ", sorted(dic4.items(), key=lambda d: d[1], reverse=True))
        if (dic3 != {}):
            print("-----------S:8002_12.2------------>>> ", sorted(dic3.items(), key=lambda d: d[1], reverse=True))

        if (len(peak4) > 0):
            print("-----------S:8002_13.1------------>>> ", df.iloc[i + peak4[0], 0])
        else:
            print("-----------S:8002_13.2------------>>> ", i, peak4)
        print("------------------------------------------------------------8002-----Final1_0------------ N--- >>>  ",lresult2)
        # print("-------------------------------------------------------------8002-----Final2_0------------ S--- >>>  ", lresult_south )
        # print("-------------------------------------------------------------8002-----Final3_0------------ S:N--- >>>  ", lresult_south[0] , " <=> ",lresult2[0] )
        fig, axes = plt.subplots(2, 2, figsize=(21, 14))  # , tight_layout=True)
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False

        axes[0, 0].plot(sect_all, sect_BB)
        axes[0, 0].plot(sect_all, sect_all[sect_BB], "xr")
        if len(lresult2) > 1 and len(lresult3) > 1:
            axes[0, 0].set_title("XY8002PI==>  洩漏.發生時間: " + str(
                df.iloc[i, 0].__str__() + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(
                    lresult3[0][0]) + "\t++ 北站1: " + str(lresult2[1][0]) + "\t<==> 南站1: " + str(lresult3[1][0])),fontsize=12, )
        elif len(lresult2) > 0 and len(lresult3) > 0:
            axes[0, 0].set_title("XY8002PI==>  洩漏.發生時間: " + str(
                df.iloc[i, 0].__str__() + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(lresult3[0][0]) ),fontsize=12, )
        else:
            axes[0, 0].set_title("XY8002PI==>  洩漏.發生時間: " + str(
                df.iloc[i, 0].__str__() + "\n北站: " +  "\t<==> 南站: " + str(lresult3[0][0]) ),fontsize=12, )
        axes[0, 0].tick_params(axis='x', rotation=75)
        axes[0, 1].plot(sect_all, sect_AA)
        axes[0, 1].set_title('Δ XY8002PI-1', fontsize=12, )
        axes[0, 1].tick_params(axis='x', rotation=75)
        # ---------------------------------------------------------------------------------------
        axes[1, 0].plot(sect_all1, sect_BB1)
        axes[1, 0].set_title('TB8002PIB', fontsize=12, )
        axes[1, 0].tick_params(axis='x', rotation=75)
        # =====================================
        axes[1, 1].plot(sect_all1, sect_AA1)
        axes[1, 1].set_title('Δ TB8002PIB-1', fontsize=12, )
        axes[1, 1].tick_params(axis='x', rotation=75)
        plt.savefig("LDS_8002_" + df.iloc[i, 0].__str__() + "_.png")
        with open('abnormal_8002.txt','a') as fs:
            fs.write("XY8002PI==>  洩漏.發生時間: " + str(
                df.iloc[i, 0].__str__() + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(
                    lresult3[0][0]) +'\n'))
        # plt.show()
        # ---------------------------------------------------------------------------------------

def find_last_peak_and_plot_8004():
    global IDx, i, sect_all, sect_A, sect_B, idx, sect_BB, sect_AA, peak2, _, dic1, dic2, lresult1, lresult2, fResult, tmp, tmp1, sect_all1, sect_A1, sect_B1, sect_BB1, sect_AA1, peak4, dic3, dic4, lresult3, lresult4, lresult_south, tmpResult, fig, axes
    IDx = 0
    tmpIndex = 2
    print("@getpeaktime2------------------------------------------------------------------------------------------------------------")
    for i in getpeaktime2:
        IDx += 1
        p8004_1 = 30
        p8004_2 = 60
        p8004_3 = 30
        # fig0,axes0 = plt.subplots(1, 1,figsize=(21,14) )
        # fig,axes = plt.subplots(1, 1,figsize=(21,14))# , tight_layout=True)
        print("============================================================================================================================")
        print("Ans--8004: "," <=> ",i, df.iloc[i, 0], " <=> ", (df.iloc[i, 5  - tmpIndex]), " <=> ", (df.iloc[i, 6 - tmpIndex]))
        print("============================================================================================================================")
        time_l.append(df.iloc[i, 0])
        if ab_flag == 1:
            replace_finalTime(df.iloc[compare2[0] * averagescale, 0], "8004", "abnormal_time2.txt")

        sect_all = df.iloc[i - p8004_1:i + p8004_2, 0]
        sect_A = []
        sect_B = []
        for idx in range(-p8004_1, p8004_2):
            sect_A.append(df.iloc[idx + i, 5  - tmpIndex] - df.iloc[idx + i + 1, 5  - tmpIndex])
            sect_B.append(df.iloc[idx + i, 5  - tmpIndex])
        sect_BB = (np.array(sect_B))
        sect_AA = (np.array(sect_A))

        # 8004 North----------------------------------------------------------------------------------------------------------->
        peak2, _ = find_peaks(sect_AA, height=0.01, width=0.1)
        # for idx in peak2:
        dic1 = {}
        dic2 = {}
        lresult1 = []
        lresult2 = []
        for idx in range(-p8004_1, p8004_2):
            if (df.iloc[i + idx, 5 - tmpIndex] - df.iloc[i + idx + 2, 5  - tmpIndex]) > 0.01:
                print(str(idx) + "). --------------N:8004_1.1--------->>> ", df.iloc[i + idx, 0], " <=> ",
                      df.iloc[i + idx, 5  - tmpIndex] - df.iloc[i + idx + 2, 5 - tmpIndex])
                dic1[str(df.iloc[i + idx, 0])] = df.iloc[i + idx, 5 - tmpIndex] - df.iloc[i + 2 + idx, 5 - tmpIndex]

        for idx in range(-p8004_1, p8004_3):
            if (df.iloc[i + idx, 5 - tmpIndex] - df.iloc[i + 2 + idx, 5 - tmpIndex]) > 0.01:
                dic2[str(df.iloc[i + idx, 0])] = df.iloc[i + idx, 5 - tmpIndex] - df.iloc[i + 2 + idx, 5 - tmpIndex]

        print("-----------N:8004_2------------>>> ", i, " <=> ", peak2, " <=> ", df.iloc[i, 0])

        if (dic2 != {}):
            lresult2 = sorted(dic2.items(), key=lambda d: d[1], reverse=True)
            # print("-----------2.4444------------>>> ", lresult2, " <=> ", type(lresult2)," <=> " ,lresult2[1], " <=> ", type(lresult2[1]), " <=> ", (lresult2[1][1]))
            print("-----------N:8004_3------------>>> ", lresult2)  # ," <=> ", lresult2[0], " <=> ", lresult2[1])

        # first= 44, sec= 21 ,sec < first , return false
        fResult = compare_2Time(lresult2[0][0], lresult2[1][0])

        if fResult == False:
            # print("1 > 0")
            tmp = lresult2[0]
            tmp1 = lresult2[1]
            lresult2[0] = tmp1
            lresult2[1] = tmp
            # print("-----------2.66666------------>>> ",lresult2)

        if (dic1 != {} and fResult == True):
            lresult1 = sorted(dic1.items(), key=lambda d: d[1], reverse=True)
            lresult2 = sorted(dic2.items(), key=lambda d: d[1], reverse=True)
            print("-----------N:8004_4.1, lresult1 = ------------>>> ", lresult1)
            print("-----------N:8004_4.2, lresult2 = ------------>>> ", lresult2)
            print("-----------N:8004_4.3,fResult = ------------>>> ", fResult)
        else:
            print("-----------N:8004_4.4, lresult2 = ------------>>> ", lresult2)
            print("-----------N:8004_4.5,fResult = ------------>>> ", fResult)

        if (len(peak2) > 0):
            print("-----------N:8004_6-------time-:-peak2--->>> ", df.iloc[i + peak2[0], 0], " : " , peak2)
        else:
            print("-----------N:8004_6.1--------peak2---->>> ", i, peak2)
        # ---------------------------------------------------------------------------------------

        # 8004 South----------------------------------------------------------------------------------------------------------->
        sect_all1 = df.iloc[i - p8004_1:i + p8004_2, 0]
        sect_A1 = []
        sect_B1 = []
        for idx in range(-p8004_1, p8004_2):
            sect_A1.append(df.iloc[idx + i, 6 - tmpIndex] - df.iloc[idx + i + 1, 6 - tmpIndex])
            sect_B1.append(df.iloc[idx + i, 6 - tmpIndex])
        sect_BB1 = (np.array(sect_B1))
        sect_AA1 = (np.array(sect_A1))

        # ---------------------------------------------------------------------------------------

        peak4, _ = find_peaks(sect_AA1, height=0.01, width=0.1)

        # for idx in peak4:
        dic3 = {}
        dic4 = {}
        lresult3 = []
        lresult4 = []

        for idx in range(-p8004_1, p8004_2):
            if (df.iloc[i + idx, 6 - tmpIndex] - df.iloc[i + 2 + idx, 6 - tmpIndex]) > 0.01:
                print(str(idx) + "). --------------S:8004_7--------->>> ", df.iloc[i + idx, 0], " <=> ",df.iloc[i + idx, 6 - tmpIndex] - df.iloc[i + 2 + idx, 6 - tmpIndex])
                dic3[str(df.iloc[i + idx, 0])] = df.iloc[i + idx, 6 - tmpIndex] - df.iloc[i + 2 + idx, 6 - tmpIndex]

        for idx in range(-p8004_1, p8004_3):
            if (df.iloc[i + idx, 6 - tmpIndex] - df.iloc[i + 2 + idx, 6 - tmpIndex]) > 0.01:
                dic4[str(df.iloc[i + idx, 0])] = df.iloc[i + idx,  6 - tmpIndex] - df.iloc[i + 2 + idx, 6 - tmpIndex]

        lresult3 = sorted(dic3.items(), key=lambda d: d[1], reverse=True)
        print("============----------S:8004_8: lresult3----------->> ", type(lresult3[0][0]), lresult3)
        tmp1 = []
        val = 0.0
        tmp2 = lresult3
        for idx in range(len(tmp2) - 1):
            val = find_1match_peakTime(tmp2[idx][0], tmp2[idx + 1][0])
            print("=============> S:8004_9 : ", val, " : ", tmp2[idx][0], " : ", tmp2[idx + 1][0])
            if (idx == 0):
                tmp1.append(tmp2[idx])
                print("=============> S:8004_9.1: ", tmp1)
            if val != 1.0 and val != -1.0 and val != 0.0:
                tmp1.append(tmp2[idx + 1])
                print("=============> S:8004_9.2 :  val:", val, type(val))

        lresult3 = tmp1
        lresult_south = []
        for idx in range(len(lresult3)):
            tmpResult = find_1match_peakTime(lresult2[0][0], lresult3[idx][0])
            print("S:8004_10============!!!>> ", lresult3[idx][0], " <=> ", lresult3[idx][1], " <=> ", tmpResult)
            if (tmpResult >= 10 and tmpResult <= 12) or (tmpResult <= -10 and tmpResult >= -12):
                print(">>>>>>>>>>>>>>>>>>>>>>>>> S:8004_11--------Got it South_0!--------  >>>>>>>>>>>>>>>>>>>> ", lresult3[idx])
                lresult_south.append(lresult3[idx])

        print("-----------S:8004_12------------>>> ", i, " <=> ", peak4, " <=> ", df.iloc[i, 0])

        if (dic4 != {}):
            print("-----------S:8004_13.1------------>>> ", sorted(dic4.items(), key=lambda d: d[1], reverse=True))
        if (dic3 != {}):
            print("-----------S:8004_13.2------------>>> ", sorted(dic3.items(), key=lambda d: d[1], reverse=True))

        if (len(peak4) > 0):
            print("-----------S:8004_14-------peak4----->>> ", df.iloc[i + peak4[0], 0], " : " , peak4)
        else:
            print("-----------S:8004_14.1------------>>> ", i, peak4)

        print("8004-----Final1------------ N--- >>>  ",lresult2)
        print("8004-----Final2------------ S--- >>>  ",lresult_south)
        print("8004-----Final3------------ S:N--- >>>  ",lresult_south[0], " <=> ", lresult2[0])

        # ---------------------------------------------------------------------------------------
        fig, axes = plt.subplots(2, 2, figsize=(21, 14))  # , tight_layout=True)
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False
        # fig,axes = plt.subplots(1, 1,figsize=(21,14))# , tight_layout=True)
        axes[0, 0].plot(sect_all, sect_BB)
        axes[0, 0].plot(sect_BB, sect_all[sect_BB], "xr")
        if len(lresult_south) > 1 and len(lresult3) > 1:
            axes[0, 0].set_title("TB8004PI==> " +  "LDS ==> 洩漏.發生時間: " + str(
                df.iloc[i, 0].__str__() + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(
                    lresult_south[0][0]) + "\t++ 北站1: " + str(lresult2[1][0]) + "\t<==> 南站1: " + str(
                    lresult_south[1][0])), fontsize=12, )
        elif len(lresult2) > 0 and len(lresult3) > 0:
            axes[0, 0].set_title("XY8004PI==>  洩漏.發生時間: " + str(
                df.iloc[i, 0].__str__() + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(lresult3[0][0]) ),fontsize=12, )
        else:
            axes[0, 0].set_title("TB8004PI==> " + "LDS ==> 洩漏.發生時間: " + str(
                df.iloc[i, 0].__str__() + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(lresult_south[0][0])),
                                 fontsize=12, )

        axes[0, 0].tick_params(axis='x', rotation=75)
        # =====================================
        axes[0, 1].plot(sect_all, sect_AA)
        # axes[0, 1].plot(sect_AA, sect_all[sect_AA], "xb")
        axes[0, 1].set_title('Δ TB8004PI-1', fontsize=12, )
        axes[0, 1].tick_params(axis='x', rotation=75)

        # ============================================================================================
        # ============================================================================================
        # ============================================================================================
        axes[1, 0].plot(sect_all1, sect_BB1)
        # axes[1, 0].plot(sect_BB1, sect_all1[sect_BB1], "xr")
        axes[1, 0].set_title('MX8004PIB-0', fontsize=12, )
        axes[1, 0].tick_params(axis='x', rotation=75)
        # =====================================
        axes[1, 1].plot(sect_all1, sect_AA1)
        # axes[1, 1].plot(sect_AA1, sect_all1[sect_AA1], "xg")
        axes[1, 1].set_title('Δ MX8004PIB-2', fontsize=12, )
        axes[1, 1].tick_params(axis='x', rotation=75)
        plt.savefig("LDS_8004_" + df.iloc[i, 0].__str__() +".png")
        with open('abnormal_8004.txt','a') as fs:
            fs.write("TB8004PI==> " +  "LDS ==> 洩漏.發生時間: " + str(
                df.iloc[i, 0].__str__() + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(
                    lresult_south[0][0]) +'\n'))
        # plt.show()
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------2022-03-26,gilbert_finish
def replace_finalTime(dateTime, pipeType ,File = 'abnormal_time.txt'):
    with open(File, 'r') as fs:
        fstream = fs.readlines()

    lastLines = fstream[len(fstream) - 1:]
    # print ("=====================> ", len(lastLines), " : " ,lastLines)
    newLine = ('=== abnormal === '+dateTime.__str__()+" " + pipeType + " pipeline\n")
    if len(lastLines) > 0:
        lastLines = fstream[len(fstream) - 1:].__str__().split()
        # print ("=====================2> ", len(lastLines), " : " ,lastLines)
    # lastLines = lastLine.__str__().split()
    # print("----------------:Hello: ", lastLines[3].split("-"), lastLines[4].split(":"))
    if lastLines != [] :
        dd = datetime((int)(lastLines[3].split("-")[0]), (int)(lastLines[3].split("-")[1]),
                               (int)(lastLines[3].split("-")[2]), (int)(lastLines[4].split(":")[0]),
                               (int)(lastLines[4].split(":")[1]), (int)(lastLines[4].split(":")[2]))
    else:
        dd = 0
    # print ("=====================3> ", dd)
    if  dd == 0 or dd > dateTime  :
        with open(File, 'w') as fs:
            for idx in range(len(fstream)-1):
                fs.write(fstream[idx])
            fs.write(newLine)

count = 0
count2 = 0
s = 0
ab_time = []
if __name__ == '__main__':
    while True:
        # Get data
        last_update = mycol.find_one({}, {'_id':0 , 'tm':1 , 'XY8002PI':1 , 'TB8002PIB':1 , 'TB8004PI':1 , 'MX8004PIB':1}, sort=[('tm', pymongo.DESCENDING)])

        end_duration = last_update['tm']
        end_duration_struct = time.strptime(end_duration.__str__(), "%Y-%m-%d %H:%M:%S")
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
            ab_flag = 0
            if count == 3000:
                count = 0
                try:
                    real_time = add_x_hours(df.iloc[239,0])

                    print('=== normal === '+str(real_time))
                    with open('now_1.csv','w') as f:
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
                    if ab_flag == 1:
                            replace_finalTime(df.iloc[compare1[0]*averagescale,0], "8002" ,"abnormal_time1.txt")

                for i in getpeaktime2:
                    time_l.append(add_x_hours(df.iloc[i, 0])+" 8004 pipeline")
                    ab_time.append(time_number(df.iloc[i, 0]))
                    if ab_flag == 1:
                            replace_finalTime(df.iloc[compare2[0]*averagescale,0], "8004" ,"abnormal_time1.txt")
                time_l.sort()

                # ab_time.append(time_number(df.iloc[i, 0]))
                if ab_time[len(ab_time)-1]>(30+ab_time[len(ab_time)-2]) or len(ab_time)==1:

                    ab_flag = 1
                    # print(ab_time[len(ab_time)-1])
                    # print(len(ab_time))
                    # print(time_l)

                    for i in time_l:
                        print('=== abnormal === '+str(i))
                        f = open('abnormal_time.txt','a')
                        f.write('=== abnormal === '+i+'\n')
                        f.close
                        with open('abnormal_time1.txt','a') as fs:
                            fs.write('=== abnormal === '+i+'\n')
                        with open('abnormal_time2.txt','a') as fs:
                            fs.write('=== abnormal === '+i+" >> alterTime >>  "+ (end_duration - timedelta(seconds=1)).__str__()+ "\n")
                        with open('abnormal_1.csv','w') as file:
                            writer = csv.writer(file)
                            ti = []
                            ti.append(i)
                            writer.writerow(ti)

                #adding by gilbert 2022-03-26 detecting south & north leak_peak
                find_last_peak_and_plot_8002()
                #adding by gilbert 2022-03-26 detecting south & north leak_peak
                find_last_peak_and_plot_8004()

