import numpy as np
import pandas as pd
import os
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

timewindow_D = []
timewindow_E = []
timewindow_F = []
timewindow_G = []

def plot_pressure(p1,p2,p3,p4,p5,p6,p7,p8):
    fig, axes = plt.subplots(4, 2, figsize=(21, 14))
    axes[0, 0].plot(p1)
    # axes[0,0].plot(peaks1, timewindow_D[peaks1],"xr")
    axes[0, 0].set_title('XY8002PI', fontsize=13)
    axes[1, 0].plot(p2)
    # axes[1,0].plot(peaks2, timewindow_E[peaks2],"xr")
    axes[1, 0].set_title('TB8002PIB', fontsize=13)
    axes[2, 0].plot(p3)
    # axes[2,0].plot(peaks3, timewindow_F[peaks3],"xb")
    axes[2, 0].set_title('TB8004PI', fontsize=13)
    axes[3, 0].plot(p4)
    # axes[3,0].plot(timewindow_G[peaks4],"xg")
    axes[3, 0].set_title('MX8004PIB', fontsize=13)
    #
    #
    axes[0, 1].plot(p5)
    # axes[0,1].plot(peaks9, delta_D_scale[peaks9],"xb")
    axes[0, 1].set_title('Δ XY8002PI', fontsize=13)
    axes[1, 1].plot(p6)
    # axes[1,1].plot(peaks10, delta_E_scale[peaks10],"xr")
    axes[1, 1].set_title('Δ TB8002PIB', fontsize=13)
    axes[2, 1].plot(p7)
    # axes[2,1].plot(peaks11, delta_F_scale[peaks11],"xg")
    axes[2, 1].set_title('Δ TB8004PI', fontsize=13)
    axes[3, 1].plot(p8)
    # axes[3,1].plot(peaks12, delta_G_scale[peaks12],"xr")
    axes[3, 1].set_title('Δ MX8004PIB', fontsize=13)
    plt.savefig(str(filename) + ".png")
    plt.show()

def hold_pressure_alter_8002(timewindow_D, timewindow_E):
    global scale ,D_delta, E_delta
    timeD = np.array(timewindow_D)
    timeE = np.array(timewindow_E)
    f1 = alter_8002_8004( timeD, timeE,D_delta, E_delta ,"8002")
    return f1

def hold_pressure_alter_8004(timewindow_F, timewindow_G):
    global scale ,F_delta, G_delta
    timeF = np.array(timewindow_F)
    timeG = np.array(timewindow_G)
    f2 = alter_8002_8004( timeF, timeG,F_delta, G_delta ,"8004")
    return f2


def alter_8002_8004(time1, time2,time1_delta, time2_delta,msgString):
    global scale
    # print("-----------------------------------------alter_8002_8004============================> ", scale ,D_delta,E_delta)
    ff= True
    flag1 = False
    flag2 = False
    for i in range(len(time1) - 3):
        d1 = time1[i + 1] - time1[i]
        d2 = time1[i + 2] - time1[i + 1]
        d3 = time1[i + 3] - time1[i + 2]
        e1 = time2[i + 1] - time2[i]
        e2 = time2[i + 2] - time2[i + 1]
        e3 = time2[i + 3] - time2[i + 2]

        if (d1 < time1_delta and d2 < time1_delta and d3 < time1_delta):
            flag1 = True
        if (e1 < time2_delta and e2 < time2_delta and e3 < time2_delta):
            flag2 = True
        if flag1 and flag2:
            ff = False
            print(msgString,"=======err time==========> ", dataframe.iloc[i * scale, 0],i * scale, i, scale )
            flag1 = False
            flag2 = False
        # else:
        #     print(msgString,"--------------------------> ", dataframe.iloc[i * scale, 0])
    return ff


def approach_final(sc,d,e,f,g,ans1,en_flag = 0):
    global scale ,D_delta, E_delta,F_delta, G_delta , scTable
    global dataframe, timewindow_D, timewindow_E, timewindow_F, timewindow_G
    scale = sc         # sampling time interval
    D_delta = -d# north trigger threshold value
    E_delta = -e# south trigger threshold value
    F_delta = -f# north trigger threshold value
    G_delta = -g# south trigger threshold value
    err_count = 0
    right_count = 0
    err_file = []
    flag = True
    for idx in range(len(all_file_list)):

        file = recur_init(idx, scale)

        err_count, right_count = print_recur_result(D_delta, E_delta, F_delta, G_delta, ans1, en_flag, err_count,
                                                    err_file, file, flag, right_count, scale, timewindow_D,
                                                    timewindow_E, timewindow_F, timewindow_G)

    # else :
    #     print(".")
    loop_request(D_delta, E_delta, F_delta, G_delta, en_flag, err_count, err_file, right_count, scale)
    if len(err_file) > 0:
        print("\n----------Final-Report_8002_8004============================> Scale: ", scale, "sec /Err: ", err_count,
              "/Right: ", right_count, "/D: ", D_delta, "/E: ", E_delta, "/F: ", F_delta, "/G: ", G_delta , "\n")


def print_recur_result(D_delta, E_delta, F_delta, G_delta, ans1, en_flag, err_count, err_file, file, flag, right_count,
                       scale, timewindow_D, timewindow_E, timewindow_F, timewindow_G):
    if en_flag == 2:
        flag = hold_pressure_alter_8002(timewindow_D, timewindow_E)
    elif en_flag == 4:
        flag = hold_pressure_alter_8004(timewindow_F, timewindow_G)
    if flag == False:
        tmp = file.strip().split("/")
        tmp = tmp[len(tmp) - 1]
        print("\n\n------------------------------------------->hold pressure  err_count: ", err_count + 1, file, ":",
              ans1[0], ":", tmp)
        print("Scale > ", scale)
        print("timewindow_D> ", D_delta)
        print("timewindow_E> ", E_delta)
        print("timewindow_F> ", F_delta)
        print("timewindow_G> ", G_delta)
        err_count += 1

        if tmp == ans1[0]:  # or tmp == ans1[1]:
            err_file.append(file)
        else:
            print("------------------------------------------->hold pressure: but not >> right answer")
    else:
        print("*:" + str(right_count + 1))
        # print("===========================================>hold pressure  right_count: ", right_count + 1, file)
        right_count += 1
    return err_count, right_count


def recur_init(idx, scale):
    global dataframe, timewindow_D, timewindow_E, timewindow_F, timewindow_G
    file = yourpath + all_file_list[idx]
    # print(all_file_list[filename])
    dataframe = pd.read_csv(file)
    dataD = dataframe['新營壓力']
    dataE = dataframe['太保壓力南']  # dataframe['太保壓力南'] #dataframe['太保壓力北']
    dataF = dataframe['太保壓力北']  # dataframe['太保壓力北'] #dataframe['太保壓力南']
    dataG = dataframe['民雄壓力']
    timewindow_D = []
    timewindow_E = []
    timewindow_F = []
    timewindow_G = []
    for i in range(1, dataframe.shape[0] // scale + 1):
        # 2" Head  xxscale sec average
        x = (dataD[i * scale - 1])
        # 2" Buttom  xxscale sec average
        y = (dataE[i * scale - 1])
        # 4" Head  xxscale sec average
        z = (dataF[i * scale - 1])
        # 4" Buttom  xxscale sec average
        w = (dataG[i * scale - 1])

        # 2" head 2880 point average
        timewindow_D.append(x)
        # 2" bottom 2880 point average
        timewindow_E.append(y)
        # 4" head 2880 point average
        timewindow_F.append(z)
        # 4" bottom 2880 point average
        timewindow_G.append(w)
    return file


def loop_request(D_delta, E_delta, F_delta, G_delta, en_flag, err_count, err_file, right_count, scale):
    Eduplicate_flag = False
    Gduplicate_flag = False
    global err_count_condition
    if err_count <= err_count_condition and len(err_file) > 0:

        if en_flag == 2:
            print("8002 alomost done===========================")
            if (eTable == []):
                eTable.append([scale, D_delta, E_delta, F_delta, G_delta])
            else:
                for idd in range(len(eTable)):
                    if eTable[idd] == [scale, D_delta, E_delta, F_delta, G_delta]:
                        Eduplicate_flag = True
                if Eduplicate_flag == False:
                    eTable.append([scale, D_delta, E_delta, F_delta, G_delta])

        if en_flag == 4:
            print("8004 almost done ===========================")
            if (gTable == []):
                gTable.append([scale, D_delta, E_delta, F_delta, G_delta])
            else:
                for idd in range(len(gTable)):
                    if gTable[idd] == [scale, D_delta, E_delta, F_delta, G_delta]:
                        Gduplicate_flag = True
                if Gduplicate_flag == False:
                    gTable.append([scale, D_delta, E_delta, F_delta, G_delta])

        with open("result7.txt", "a") as fp:
            fp.write("\n----------Final-Report_8002_8004============================> Scale: " + str(scale) + "sec /Err: " + str(
                    err_count) +"/Right: " + str(right_count) + "/D: " + str(D_delta) + "/E: " + str(E_delta) + "/F: " + str(
                    F_delta) + "/G: " + str(G_delta))


def print_result():
    print(scTable)
    print("dTable > ", dTable)
    print("eTable > ", eTable)
    print("fTable > ", fTable)
    print("gTable > ", gTable)


def loop_in_8002_8004():
    global err_count_condition,start_8002,start_8004,end_8004,end_8002,loop_count_interval
    for id1 in range(start_8002, end_8002, loop_count_interval):
        print("\nloop_in_8002_8004 ==========================> 8002",id1)
        # for id2 in range(len(fTable)):
        for id2 in range(1, 10):
            # print("\n6 ==========================> fTable",fTable)
            for id3 in range(1, 10):
                # print("\n7 =====> fTable", fTable[id2][0] , -1*fTable[id2][1] , fTable[id2][1] , id5)
                # approach_final(fTable[id2][0],0.01,0.05,-1*fTable[id2][1],0.01*id5,ans_80021,4)
                approach_final(id1, 1 * 0.01 * id2, 0.01 * id3, 0.02, 0.015, ans_8002, 2)

    for id1 in range(start_8004, end_8004,  loop_count_interval):
        print("\nloop_in_8002_8004 ==========================> 8004",id1)
        for id2 in range(1, 10):
            # print("\n6 ==========================> fTable",fTable)
            for id5 in range(14, 16):
                # print("\n7 =====> fTable", fTable[id2][0] , -1*fTable[id2][1] , fTable[id2][1] , id5)
                # approach_final(fTable[id2][0],0.01,0.05,-1*fTable[id2][1],0.01*id5,ans_8004,4)
                approach_final(id1, 0.01, 0.05, 1 * 0.01 * id2, 0.001 * id5, ans_8004, 4)


if __name__ == '__main__':
    scTable = []
    dTable = []
    eTable = []
    fTable = []
    gTable = []

    ans_8002 = ["202203220000-202203222359.csv"]
    ans_8004 = ["202203240000-202203242359.csv"]

    global err_count_condition,start_8002,start_8004,end_8004,end_8002,loop_count_interval
    err_count_condition = 4
    start_8002 = 100
    start_8004 = 100
    end_8002 = 1000
    end_8004 = 1000
    loop_count_interval = 100

    # sampling time interval
    scale = 900

    # initial value
    D_delta = -0.01
    E_delta = -0.05
    F_delta = -0.02
    G_delta = -0.015
    filename = 0

    yourpath = '/home/gilbert3/Downloads/leak數據/'
    all_file_list = os.listdir(yourpath)
    all_file_list = sorted(all_file_list)

    loop_in_8002_8004()

    print_result()
    # plot_pressure(timewindow_D,timewindow_E,timewindow_F,timewindow_G,timewindow_D,timewindow_E,timewindow_F,timewindow_G)
