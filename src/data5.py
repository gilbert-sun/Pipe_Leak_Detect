import numpy as np
import pandas as pd
import os
# import matplotx
from time import strptime,mktime
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
yourpath = '/home/gilbert3/Downloads/leak數據/'
all_file_list = os.listdir(yourpath)
all_file_list = sorted(all_file_list)
filename = 0
file = yourpath + all_file_list[filename]
print(all_file_list[filename])
dataframe = pd.read_csv(file)



dataD = dataframe['新營壓力']
dataE = dataframe['太保壓力南'] #dataframe['太保壓力南'] #dataframe['太保壓力北']
dataF = dataframe['新營壓力'] #dataframe['太保壓力北'] #dataframe['太保壓力南']
dataG = dataframe['太保壓力南']
#
# dataD = dataframe['XY8002PI']
# dataE = dataframe['TB8002PIB']
# dataF = dataframe['TB8004PI']
# dataG = dataframe['MX8004PIB']

def compare_8002North(NorthPeak,SouthPeak):
    # struct1 = strptime((NorthPeak), "%Y-%m-%d %H:%M:%S")
    # NT = mktime(struct1)
    # struct2 = strptime((SouthPeak), "%Y-%m-%d %H:%M:%S")
    # ST = mktime(struct2)
    #ST = 23 / NT = 41
    #ST = 23 / NT = 21
    #ST = 21 / NT = 44
    if int(float(SouthPeak)*1000) - int(float(NorthPeak)*1000) > 0:
        return False
    elif int(float(SouthPeak)*1000) -  int(float(NorthPeak)*1000) > 0 and int(float(SouthPeak)*1000) -  int(float(NorthPeak)*1000) < 60:
        return False
    elif  int(float(NorthPeak)*1000) - int(float(SouthPeak)*1000) > 40:
        return True


def compare_8004North(NorthPeak,SouthPeak):
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
    # struct1 = strptime((NorthPeak), "%Y-%m-%d %H:%M:%S")
    # NT = mktime(struct1)
    # struct2 = strptime((SouthPeak), "%Y-%m-%d %H:%M:%S")
    # ST = mktime(struct2)
    return int(float(SouthPeak)*1000) -  int(float(NorthPeak)*1000)

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

def replace_finalTime(dateTime, pipeType ,File = 'abnormal_time.txt'):
    # print ("=====================2> ", type(dateTime))
    with open(File, 'r') as fs:
        fstream = fs.readlines()

    lastLines = fstream[len(fstream) - 1:]
    # print ("=====================> ", len(lastLines), " <=> " ,lastLines)
    newLine = ('=== abnormal === '+dateTime.__str__()+" " + pipeType + " pipeline\n")
    if len(lastLines) > 0:
        lastLines = fstream[len(fstream) - 1:].__str__().split()
        # print ("=====================2> ", len(lastLines), " <=> " ,lastLines)
    # lastLines = lastLine.__str__().split()
    # print("----------------:Hello: ", lastLines[3].split("-"), lastLines[4].split(":"))
    if lastLines != [] :
        dd = datetime((int)(lastLines[3].split("-")[0]), (int)(lastLines[3].split("-")[1]),
                      (int)(lastLines[3].split("-")[2]), (int)(lastLines[4].split(":")[0]),
                      (int)(lastLines[4].split(":")[1]), (int)(lastLines[4].split(":")[2]))
    else:
        dd = 0
    # print ("=====================3> ", dd, " <=> ",type(dateTime))
    #fTime + timedelta(seconds=30)) >= dateTime
    dateTime = datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
    if  dd == 0 or dd > dateTime  :
        with open(File, 'w') as fs:
            for idx in range(len(fstream)-1):
                fs.write(fstream[idx])
            fs.write(newLine)

def rms(scores):
    return np.sqrt(np.mean(scores**2))
def average(scores):
    return np.mean(scores)

scale = 30
timewindow_D = []
timewindow_E = []
timewindow_F = []
timewindow_G = []


def find_last_peak_and_plot_8002():
    global IDx, i, sect_all, sect_A, sect_B, idx, sect_BB, sect_AA, peak2, _, dic1, dic2, lresult1, lresult2, fResult, tmp, tmp1, sect_all1, sect_A1, sect_B1, sect_BB1, sect_AA1, peak4, dic3, dic4, lresult3, lresult4, lresult_south, tmpResult, fig, axes
    IDx = 0
    print("#getpeaktime1------------------------------------------------------------------------------------------------------------")
    for i in getpeaktime1:
        print("============================================================================================================================")
        print("Ans--8002: "," <=> ",i, dataframe.iloc[i, 0], " <=> ", type(dataframe.iloc[i, 0]))
        print("============================================================================================================================")
        time_l.append(dataframe.iloc[i, 0])

        IDx += 1
        p8002_1 = 30
        p8002_2 = 60
        p8002_3 = 30
        sect_all = dataframe.iloc[i - p8002_1:i + p8002_2, 0]
        sect_A = []
        sect_B = []
        for idx in range(-p8002_1, p8002_2):
            sect_A.append(dataframe.iloc[idx + i, 1] - dataframe.iloc[idx + i + 1, 1])
            sect_B.append(dataframe.iloc[idx + i, 1])
        sect_BB = (np.array(sect_B))
        sect_AA = (np.array(sect_A))

        #8002 _ North---------------------------------------------------------------------------------------------------------
        peak2, _ = find_peaks(sect_AA, height=0.01, width=0.1)
        dic1 = {}
        dic2 = {}
        lresult1 = []
        lresult2 = []
        for idx in range(-p8002_1, p8002_2):
            if (dataframe.iloc[i + idx, 1] - dataframe.iloc[i + idx + 2, 1]) > 0.01:
                print(str(idx) + "). --------------N:8002_1--------->>> ", dataframe.iloc[i + idx, 0], " <=> ",
                      dataframe.iloc[i + idx, 1] - dataframe.iloc[i + idx + 2, 1])
                dic1[str(dataframe.iloc[i + idx, 0])] = dataframe.iloc[i + idx, 1] - dataframe.iloc[i + 2 + idx, 1]
                lresult2.append([str(dataframe.iloc[i + idx, 0]),dataframe.iloc[i + idx, 1] - dataframe.iloc[i + 2 + idx, 1]])

        for idx in range(-p8002_1, p8002_3):
            if (dataframe.iloc[i + idx, 1] - dataframe.iloc[i + 2 + idx, 1]) > 0.01:
                dic2[str(dataframe.iloc[i + idx, 0])] = dataframe.iloc[i + idx, 1] - dataframe.iloc[i + 2 + idx, 1]
                lresult2.append([str(dataframe.iloc[i + idx, 0]),dataframe.iloc[i + idx, 1] - dataframe.iloc[i + 2 + idx, 1]])

        print("-----------N:8002_2------------>>> ", i, " <=> ", peak2, " <=> ", dataframe.iloc[i, 0])

        if (dic2 != {}):
            # lresult2 = sorted(dic2.items(), key=lambda d: d[1], reverse=True)
            print("-----------N:8002_3.1------------>>> ", lresult2)  # ," <=> ", lresult2[0], " <=> ", lresult2[1])
        elif (dic1 != {}):
            # lresult2 = sorted(dic1.items(), key=lambda d: d[1], reverse=True)
            print("-----------N:8002_3.2------------>>> ", lresult2)  # ," <=> ", lresult2[0], " <=> ", lresult2[1])
        if len(lresult2) > 1:
            fResult = compare_8002North(lresult2[0][0], lresult2[1][0])
        else:
            fResult = False
        print("============---N:8002_4-------lresult12----------->> ", lresult2)
        if fResult == True:
            tmp = lresult2[0]
            tmp1 = lresult2[1]
            lresult2[0] = tmp1
            lresult2[1] = tmp

        if (dic1 != {} and fResult == True):

            lresult1 = sorted(dic1.items(), key=lambda d: d[1], reverse=True)
            lresult2 = sorted(dic2.items(), key=lambda d: d[1], reverse=True)
            print("-----------N:8002_4_1, lresult1 = ------------>>> ", lresult1)
            print("-----------N:8002_4_1.1, lresult2 = ------------>>> ", lresult2)
            print("-----------N:8002_4_1.1, fResult = ------------>>> ", fResult)
        else:
            print("-----------N:8002_4_2, lresult2 = ------------>>> ", lresult2)
            print("-----------N:8002_4_2.1,fResult = ------------>>> ", fResult)

        print("============---N:8002_5-------lresult12----------->> ", lresult2)

        if (len(peak2) > 0):
            print("-----------N:8002_6.1---------peak2--->>> ", dataframe.iloc[i + peak2[0], 0]," : ",peak2)
        else:
            print("-----------N:8002_6_2------------>>> ", i, peak2)

        # 8002 _ South---------------------------------------------------------------------------------------

        sect_all1 = dataframe.iloc[i - p8002_1:i + p8002_2, 0]
        sect_A1 = []
        sect_B1 = []
        for idx in range(-p8002_1, p8002_2):
            sect_A1.append(dataframe.iloc[idx + i, 2] - dataframe.iloc[idx + i + 1, 2])
            sect_B1.append(dataframe.iloc[idx + i, 2])
        sect_BB1 = (np.array(sect_B1))
        sect_AA1 = (np.array(sect_A1))

        peak4, _ = find_peaks(sect_AA1, height=0.01, width=0.1)
        dic3 = {}
        dic4 = {}
        lresult3 = []
        lresult4 = []

        for idx in range(-p8002_1, p8002_2):
            if (dataframe.iloc[i + idx, 2] - dataframe.iloc[i + 2 + idx, 2]) > 0.01:
                print(str(idx) + "). --------------S:8002_7--------->>> ", dataframe.iloc[i + idx, 0], " <=> ",
                      dataframe.iloc[i + idx, 2] - dataframe.iloc[i + 2 + idx, 2])
                dic3[str(dataframe.iloc[i + idx, 0])] = dataframe.iloc[i + idx, 2] - dataframe.iloc[i + 2 + idx, 2]
                lresult3.append( [str(dataframe.iloc[i + idx, 0]),dataframe.iloc[i + idx, 2] - dataframe.iloc[i + 2 + idx, 2]] )

        for idx in range(-p8002_1, p8002_3):
            if (dataframe.iloc[i + idx, 2] - dataframe.iloc[i + 2 + idx, 2]) > 0.01:
                dic4[str(dataframe.iloc[i + idx, 0])] = dataframe.iloc[i + idx, 2] - dataframe.iloc[i + 2 + idx, 2]
                lresult3.append( [str(dataframe.iloc[i + idx, 0]),dataframe.iloc[i + idx, 2] - dataframe.iloc[i + 2 + idx, 2]] )

        # lresult3 = sorted(dic3.items(), key=lambda d: d[1], reverse=True)
        print("============----------S:8002_8  ------ lresult3:----------->> ", lresult3)

        lresult_south = []
        # find south - north >= 10 && <=12 , south =32 later, north = 22
        for idx in range(len(lresult3)):
            if lresult2 != []:
                tmpResult = find_1match_peakTime(lresult2[0][0], lresult3[idx][0])
            print("S:8002_9============!!!>> ", lresult3[idx][0], " <=> ", lresult3[idx][1], " <=> ", tmpResult)
            # if (tmpResult >= 9 and tmpResult <= 23) or (tmpResult <= -9 and tmpResult >= -23):
            if (tmpResult >=1 and tmpResult <= 60) or (tmpResult <= -1 and tmpResult >= -40):
                print(">>>>>>>>>>>>>>>>>>>>>>>>> --------S:8002_10 : Got it South_0!--------  >>>>>>>>>>>>>>>>>>>> ", lresult3[idx])
                lresult_south.append(lresult3[idx])

        print("-----------S:8002_11------------>>> ", i, " <=> ", peak4, " <=> ", dataframe.iloc[i, 0])

        if (dic4 != {}):
            print("-----------S:8002_12.1------------>>> ", sorted(dic4.items(), key=lambda d: d[1], reverse=True))
        if (dic3 != {}):
            print("-----------S:8002_12.2------------>>> ", sorted(dic3.items(), key=lambda d: d[1], reverse=True))

        if (len(peak4) > 0):
            print("-----------S:8002_13.1------------>>> ", dataframe.iloc[i + peak4[0], 0])
        else:
            print("-----------S:8002_13.2------------>>> ", i, peak4)
        print("------------------------------------------------------------8002-----Final1_0------------ N--- >>>  ",lresult2)
        print("-------------------------------------------------------------8002-----Final2_0------------ S--- >>>  ", lresult_south )
        # print("-------------------------------------------------------------8002-----Final3_0------------ S:N--- >>>  ", lresult_south[0] , " <=> ",lresult2[0] )
        fig, axes = plt.subplots(2, 2, figsize=(21, 14))  # , tight_layout=True)
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False

        axes[0, 0].plot(sect_all, sect_BB)
        # axes[0, 0].plot(sect_all, sect_all[sect_BB], "xr")
        if len(lresult2) > 1 and len(lresult3) > 1:
            axes[0, 0].set_title("XY8002PI==> " + str(all_file_list[0].split(".")[0].split("_")[0]+".csv") + str("==> Leakage.HappenTime: " ) + str(
                dataframe.iloc[i, 0]) + str("\nNorth: " ) + str(lresult2[0][0]) + str("\t<==> South: ") + str(lresult3[0][0]) ,fontsize=12, )
        else :
            axes[0, 0].set_title("XY8002PI==> " + all_file_list[0].split(".")[0].split("_")[0]+ "==> 洩漏.發生時間: " + str(
                dataframe.iloc[i, 0])+ "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(lresult3[0][0] ),fontsize=12, )
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
        plt.savefig(str(filename) + "_" + str(i) + "2_.png")
        plt.show()
        # with open('abnormal_8002.txt','a') as fs:
        #     fs.write("XY8002PI==>  洩漏.發生時間: " + str(
        #         dataframe.iloc[i, 0].__str__() + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(
        #             lresult3[0][0]) +'\n'))
        # ---------------------------------------------------------------------------------------


def find_last_peak_and_plot_8004():
    global IDx, i, sect_all, sect_A, sect_B, idx, sect_BB, sect_AA, peak2, _, dic1, dic2, lresult1, lresult2, fResult, tmp, tmp1, sect_all1, sect_A1, sect_B1, sect_BB1, sect_AA1, peak4, dic3, dic4, lresult3, lresult4, lresult_south, tmpResult, fig, axes
    IDx = 0
    print("@getpeaktime2------------------------------------------------------------------------------------------------------------")
    for i in getpeaktime2:
        IDx += 1
        p8004_1 = 30
        p8004_2 = 60
        p8004_3 = 30
        # fig0,axes0 = plt.subplots(1, 1,figsize=(21,14) )
        # fig,axes = plt.subplots(1, 1,figsize=(21,14))# , tight_layout=True)
        print("============================================================================================================================")
        print("Ans--8004: "," <=> ",i, dataframe.iloc[i, 0], " <=> ", type(dataframe.iloc[i, 0]))
        print("============================================================================================================================")
        time_l.append(dataframe.iloc[i, 0])
        if ab_flag == 1:
            replace_finalTime(dataframe.iloc[compare2[0] * averagescale, 0], "8004", "abnormal_time2.txt")

        sect_all = dataframe.iloc[i - p8004_1:i + p8004_2, 0]
        sect_A = []
        sect_B = []
        for idx in range(-p8004_1, p8004_2):
            sect_A.append(dataframe.iloc[idx + i, 5] - dataframe.iloc[idx + i + 1, 5])
            sect_B.append(dataframe.iloc[idx + i, 5])
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
            if (dataframe.iloc[i + idx, 5] - dataframe.iloc[i + idx + 2, 5]) > 0.001:
                print(str(idx) + "). --------------N:8004_1.1--------->>> ", dataframe.iloc[i + idx, 0], " <=> ",
                      dataframe.iloc[i + idx, 5] - dataframe.iloc[i + idx + 2, 5])
                dic1[str(dataframe.iloc[i + idx, 0])] = dataframe.iloc[i + idx, 5] - dataframe.iloc[i + 2 + idx, 5]

        for idx in range(-p8004_1, p8004_3):
            if (dataframe.iloc[i + idx, 5] - dataframe.iloc[i + 2 + idx, 5]) > 0.001:
                dic2[str(dataframe.iloc[i + idx, 0])] = dataframe.iloc[i + idx, 5] - dataframe.iloc[i + 2 + idx, 5]
                lresult2.append([str(dataframe.iloc[i + idx, 0]),dataframe.iloc[i + idx, 5] - dataframe.iloc[i + 2 + idx, 5]])
        print("-----------N:8004_2------------>>> ", i, " <=> ", peak2, " <=> ", dataframe.iloc[i, 0])

        if (dic2 != {}):
            # lresult2 = sorted(dic2.items(), key=lambda d: d[1], reverse=True)
            # print("-----------2.4444------------>>> ", lresult2, " <=> ", type(lresult2)," <=> " ,lresult2[1], " <=> ", type(lresult2[1]), " <=> ", (lresult2[1][1]))
            print("-----------N:8004_3------------>>> ", lresult2)  # ," <=> ", lresult2[0], " <=> ", lresult2[1])

        # first= 44, sec= 21 ,sec < first , return false
        fResult = compare_8004North(lresult2[0][0], lresult2[1][0])

        # if fResult == False:
        #     # print("1 > 0")
        #     tmp = lresult2[0]
        #     tmp1 = lresult2[1]
        #     lresult2[0] = tmp1
        #     lresult2[1] = tmp
            # print("-----------2.66666------------>>> ",lresult2)

        # if (dic1 != {} and fResult == True):
        #     lresult1 = sorted(dic1.items(), key=lambda d: d[1], reverse=True)
        #     lresult2 = sorted(dic2.items(), key=lambda d: d[1], reverse=True)
        #     print("-----------N:8004_4.1, lresult1 = ------------>>> ", lresult1)
        #     print("-----------N:8004_4.2, lresult2 = ------------>>> ", lresult2)
        #     print("-----------N:8004_4.3,fResult = ------------>>> ", fResult)
        # else:
        #     print("-----------N:8004_4.4, lresult2 = ------------>>> ", lresult2)
        #     print("-----------N:8004_4.5,fResult = ------------>>> ", fResult)

        if (len(peak2) > 0):
            print("-----------N:8004_6-------time-:-peak2--->>> ", dataframe.iloc[i + peak2[0], 0], " : " , peak2)
        else:
            print("-----------N:8004_6.1--------peak2---->>> ", i, peak2)
        # ---------------------------------------------------------------------------------------

        # 8004 South----------------------------------------------------------------------------------------------------------->
        sect_all1 = dataframe.iloc[i - p8004_1:i + p8004_2, 0]
        sect_A1 = []
        sect_B1 = []
        for idx in range(-p8004_1, p8004_2):
            sect_A1.append(dataframe.iloc[idx + i, 6] - dataframe.iloc[idx + i + 1, 6])
            sect_B1.append(dataframe.iloc[idx + i, 6])
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
            if (dataframe.iloc[i + idx, 6] - dataframe.iloc[i + 2 + idx, 6]) > 0.001:
                print(str(idx) + "). --------------S:8004_7--------->>> ", dataframe.iloc[i + idx, 0], " <=> ",dataframe.iloc[i + idx, 6] - dataframe.iloc[i + 2 + idx, 6])
                dic3[str(dataframe.iloc[i + idx, 0])] = dataframe.iloc[i + idx, 6] - dataframe.iloc[i + 2 + idx, 6]

        for idx in range(-p8004_1, p8004_3):
            if (dataframe.iloc[i + idx, 6] - dataframe.iloc[i + 2 + idx, 6]) > 0.001:
                dic4[str(dataframe.iloc[i + idx, 0])] = dataframe.iloc[i + idx, 6] - dataframe.iloc[i + 2 + idx, 6]
                lresult3.append( [str(dataframe.iloc[i + idx, 0]),dataframe.iloc[i + idx, 6] - dataframe.iloc[i + 2 + idx, 6]] )

        # lresult3 = sorted(dic3.items(), key=lambda d: d[1], reverse=True)
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
            if (tmpResult >= 9 and tmpResult <= 23) or (tmpResult <= -9 and tmpResult >= -23):
                print(">>>>>>>>>>>>>>>>>>>>>>>>> S:8004_11--------Got it South_0!--------  >>>>>>>>>>>>>>>>>>>> ", lresult3[idx])
                lresult_south.append(lresult3[idx])

        print("-----------S:8004_12------------>>> ", i, " <=> ", peak4, " <=> ", dataframe.iloc[i, 0])

        if (dic4 != {}):
            print("-----------S:8004_13.1------------>>> ", sorted(dic4.items(), key=lambda d: d[1], reverse=True))
        if (dic3 != {}):
            print("-----------S:8004_13.2------------>>> ", sorted(dic3.items(), key=lambda d: d[1], reverse=True))

        if (len(peak4) > 0):
            print("-----------S:8004_14-------peak4----->>> ", dataframe.iloc[i + peak4[0], 0], " : " , peak4)
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
        if len(lresult_south) > 1:
            axes[0, 0].set_title("TB8004PI==> " + all_file_list[0].split(".")[0].split("_")[1] + "==> 洩漏.發生時間: " + str(
                dataframe.iloc[i, 0] + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(
                    lresult_south[0][0]) + "\t++ 北站1: " + str(lresult2[1][0]) + "\t<==> 南站1: " + str(
                    lresult_south[1][0])), fontsize=12, )
        else:
            axes[0, 0].set_title("TB8004PI==> " + all_file_list[0].split(".")[0].split("_")[1] + "==> 洩漏.發生時間: " + str(
                dataframe.iloc[i, 0] + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(lresult_south[0][0])),
                                 fontsize=12, )
        axes[0, 0].tick_params(axis='x', rotation=75)

        # =====================================
        axes[0, 1].plot(sect_all, sect_AA)
        axes[0, 1].plot(sect_AA, sect_all[sect_AA], "xb")
        axes[0, 1].set_title('Δ TB8004PI-1', fontsize=12, )
        axes[0, 1].tick_params(axis='x', rotation=75)

        # ============================================================================================
        # ============================================================================================
        # ============================================================================================
        axes[1, 0].plot(sect_all1, sect_BB1)
        axes[1, 0].plot(sect_BB1, sect_all1[sect_BB1], "xr")
        axes[1, 0].set_title('MX8004PIB-0', fontsize=12, )
        axes[1, 0].tick_params(axis='x', rotation=75)
        # =====================================
        axes[1, 1].plot(sect_all1, sect_AA1)
        axes[1, 1].plot(sect_AA1, sect_all1[sect_AA1], "xg")
        axes[1, 1].set_title('Δ MX8004PIB-2', fontsize=12, )
        axes[1, 1].tick_params(axis='x', rotation=75)
        plt.savefig(str(filename) + "_" + str(i) + "2_.png")
        plt.show()
        with open('abnormal_8004.txt','a') as fs:
            fs.write("TB8004PI==> " +  "LDS ==> 洩漏.發生時間: " + str(
                dataframe.iloc[i, 0].__str__() + "\n北站: " + str(lresult2[0][0]) + "\t<==> 南站: " + str(
                    lresult_south[0][0]) +'\n'))


if __name__ == '__main__':
    ab_flag = 0
    averagescale = 30
    print("--0.5: ",type(dataframe.shape[0]),dataframe.shape[0])
    print("--0.51: ",type(dataD),dataD.shape[0],)
    # 86400 point[sec]  to 2880 point ==> //scale = 30
    for i in range(dataframe.shape[0]//scale):
        # 2" Head  30 sec average
        x = average(np.array(dataD[i*scale:(i+1)*scale]))
        # 2" Buttom  30 sec average
        y = average(np.array(dataE[i*scale:(i+1)*scale]))
        # 4" Head  30 sec average
        z = average(np.array(dataF[i*scale:(i+1)*scale]))
        # 4" Buttom  30 sec average
        w = average(np.array(dataG[i*scale:(i+1)*scale]))


        #2" head 2880 point average
        timewindow_D.append(x)
        #2" bottom 2880 point average
        timewindow_E.append(y)
        #4" head 2880 point average
        timewindow_F.append(z)
        #4" bottom 2880 point average
        timewindow_G.append(w)


    print("--0.6: ",type(timewindow_D),len(timewindow_D))#,type(Average_D),len(Average_D),)
    timewindow_D = np.array(timewindow_D)
    print("--0.7: ",type(timewindow_D),len(timewindow_D),type(timewindow_F),len(timewindow_F),)
    timewindow_E = np.array(timewindow_E)
    timewindow_F = np.array(timewindow_F)
    timewindow_G = np.array(timewindow_G)


    delta_D_scale = []
    delta_E_scale = []
    delta_F_scale = []
    delta_G_scale = []

    print("--0.8: ",type(timewindow_D),timewindow_F.shape[0])

    # back - front , count 147 - 1, lastone assign 0
    for i in range(timewindow_F.shape[0]):
        if i < timewindow_F.shape[0]-1:
            delta_D_scale.append(timewindow_D[i+1] - timewindow_D[i])
            delta_E_scale.append(timewindow_E[i+1] - timewindow_E[i])
            delta_F_scale.append(timewindow_F[i+1] - timewindow_F[i])
            delta_G_scale.append(timewindow_G[i+1] - timewindow_G[i])
        else:
            delta_D_scale.append(0)
            delta_E_scale.append(0)
            delta_F_scale.append(0)
            delta_G_scale.append(0)

    print("-------------------------------0.81: ")
    # slope from negtive to become positive
    delta_D_scale = -(np.array(delta_D_scale))
    delta_E_scale = -(np.array(delta_E_scale))
    delta_F_scale = -(np.array(delta_F_scale))
    delta_G_scale = -(np.array(delta_G_scale))

    #======================================================================================
    delta_D = []
    delta_E = []
    delta_F = []
    delta_G = []

    # print("--0.9: ",type(delta_D_scale),len(delta_D_scale))

    for num in delta_D_scale:
        for i in range(scale):
            delta_D.append(num)

    print("--0.9: ",type(delta_D_scale),len(delta_D_scale),type(delta_D),len(delta_D))
    # for i in range(du):
    #     delta_D.append(0)
    for num in delta_E_scale:
        for i in range(scale):
            delta_E.append(num)
    # for i in range(du):
    #     delta_E.append(0)
    for num in delta_F_scale:
        for i in range(scale):
            delta_F.append(num)
    # for i in range(du):
    #     delta_F.append(0)
    for num in delta_G_scale:
        for i in range(scale):
            delta_G.append(num)
    #======================================================================================
    peaks1, _ = find_peaks(timewindow_D, height=0.001, distance = 500, width=1)
    peaks2, _ = find_peaks(timewindow_E, height=0.001, distance = 500, width=1)
    peaks3, _ = find_peaks(timewindow_F, height=0.001, distance = 500, width=1)
    peaks4, _ = find_peaks(timewindow_G, height=0.001, distance = 500, width=1)
    # peaks5, _ = find_peaks(timewindow_delta_D, distance = 500)
    # peaks6, _ = find_peaks(timewindow_delta_E, distance = 500)
    # peaks7, _ = find_peaks(timewindow_delta_F, distance = 500)
    # peaks8, _ = find_peaks(timewindow_delta_G, distance = 500)
    peaks9, peaks91 = find_peaks(delta_D_scale, height=0.005,  width=1.5)
    peaks10, peaks101 = find_peaks(delta_E_scale, height=0.005, width=1.5)
    peaks11, _ = find_peaks(delta_F_scale, height=0.005,width=1.5)
    peaks12, _ = find_peaks(delta_G_scale, height=0.005,width=1.5)


    # print("------")
    # print("--0.91: ",type(peaks9),len(peaks9), peaks9)
    # print("--0.92: ",type(peaks91),len(peaks91))
    # print("------")
    # print("--0.93: ",type(peaks10),len(peaks10), peaks10)
    # print("--0.94: ",type(peaks101),len(peaks101))
    # print("------")
    # print("--0.95: ",type(peaks11),len(peaks11), peaks11)
    # print("------")
    # print("--0.96: ",type(peaks12),len(peaks12), peaks12)
    # print("------")
    # for k,v in peaks91.items():
    #     print(k,v)
    #=================================================================
    # fig,axes = plt.subplots(4, 2, figsize=(21,14) )
    # axes[0,0].plot(timewindow_D)
    # axes[0,0].plot(peaks1, timewindow_D[peaks1],"xr")
    # axes[0,0].set_title('XY8002PI', fontsize=13)
    # axes[1,0].plot(timewindow_E)
    # axes[1,0].plot(peaks2, timewindow_E[peaks2],"xr")
    # axes[1,0].set_title('TB8002PIB', fontsize=13)
    # axes[2,0].plot(timewindow_F)
    # axes[2,0].plot(peaks3, timewindow_F[peaks3],"xr")
    # axes[2,0].set_title('TB8004PI', fontsize=13)
    # axes[3,0].plot(timewindow_G)
    # axes[3,0].plot(peaks4, timewindow_G[peaks4],"xr")
    # axes[3,0].set_title('MX8004PIB', fontsize=13)
    #
    #
    # axes[0,1].plot(delta_D_scale)
    # axes[0,1].plot(peaks9, delta_D_scale[peaks9],"xb")
    # axes[0,1].set_title('Δ XY8002PI', fontsize=13)
    # axes[1,1].plot(delta_E_scale)
    # axes[1,1].plot(peaks10, delta_E_scale[peaks10],"xr")
    # axes[1,1].set_title('Δ TB8002PIB', fontsize=13)
    # axes[2,1].plot(delta_F_scale)
    # axes[2,1].plot(peaks11, delta_F_scale[peaks11],"xg")
    # axes[2,1].set_title('Δ TB8004PI', fontsize=13)
    # axes[3,1].plot(delta_G_scale)
    # axes[3,1].plot(peaks12, delta_G_scale[peaks12],"xr")
    # axes[3,1].set_title('Δ MX8004PIB', fontsize=13)
    # print ("1------------------------------> ",delta_D_scale[peaks9], " :> " , peaks9 , " :> ",len(peaks9), " :> " , len(delta_D_scale)," =>  " ,type(delta_D_scale) ,len(delta_D_scale[peaks9]))
    # print ("2------------------------------> ",delta_E_scale[peaks10], " :> " , peaks10 , " :> ",len(peaks10), " :> " , len(delta_E_scale)," =>  " ,type(delta_E_scale) ,len(delta_E_scale[peaks10]))
    # print ("3------------------------------> ",delta_F_scale[peaks11], " :> " , type(peaks11) , " :> ",len(peaks11), " :> " , len(delta_F_scale)," =>  " ,type(delta_F_scale) ,type(delta_F_scale[peaks11]))
    # print ("4------------------------------> ",delta_G_scale[peaks12], " :> " ,type( peaks12) , " :> ",len(peaks12), " :> " , len(delta_G_scale)," =>  " ,type(delta_G_scale) ,type(delta_G_scale[peaks12]))
    # plt.savefig(str(filename)+".png")
    # plt.show()
    #=================================================================

    compare1 = list(peaks9)+list(peaks10)
    compare2 = list(peaks11)+list(peaks12)
    compare1.sort()
    compare2.sort()
    getpeak1 = []
    getpeak2 = []

    for i in range(len(compare1)-1):
        if abs(compare1[i]-compare1[i+1])<2 :
            getpeak1.append(compare1[i])
            print("--1: ",i,compare1[i])
    print("------")
    print("--1.1: ",type(getpeak1),len(getpeak1), getpeak1)
    print("--1.2: ",type(compare1),len(compare1), compare1)

    getpeaktime1 = np.array(getpeak1)*scale

    print("--1.3: ",type(getpeaktime1),len(getpeaktime1), getpeaktime1)
    for i in range(len(compare2)-1):
        if abs(compare2[i]-compare2[i+1])<2:
            getpeak2.append(compare2[i])
            print("--2: ",i,compare2[i])
    print("------")
    print("--2.1: ",type(getpeak2),len(getpeak2), getpeak2)
    print("--2.2: ",type(compare2),len(compare2), compare2)
    getpeaktime2 = np.array(getpeak2)*scale
    print("------")
    # print("--3: ",dataframe.iloc[:])
    time_l = []
    if getpeaktime1.shape[0] <= 0 and getpeaktime2.shape[0] <= 0:
        ab_flag = 0
        print('=== normal ===')
    else:
        print('=== abnormal ===')
        #------------------------------------------------------------------------------------------------------------
        time_l.sort()
        ab_flag = 1
        for i in time_l:
            print(i)
            path = 'output.txt'
            f = open(path, 'a')

            f.write(i+'\n')
            f.close()

            with open('abnormal_time2.txt','a') as fs:
                fs.write('=== abnormal === '+i+'\n')
        #------------------------------------------------------------------------------------------------------------
        find_last_peak_and_plot_8002()

        #------------------------------------------------------------------------------------------------------------
        # find_last_peak_and_plot_8004()