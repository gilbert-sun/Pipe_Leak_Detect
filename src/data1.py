import numpy as np
import pandas as pd
import os
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

yourpath = '/home/gilbert3/Downloads/leak數據/'
all_file_list = os.listdir(yourpath)
all_file_list = sorted(all_file_list)
filename = 0
file = yourpath + all_file_list[filename]
print(all_file_list[filename])
dataframe = pd.read_csv(file)


#
# dataD = dataframe['新營壓力']
# dataE = dataframe['太保壓力南'] #dataframe['太保壓力北']
# dataF = dataframe['太保壓力北'] #dataframe['太保壓力南']
# dataG = dataframe['民雄壓力']

dataD = dataframe['XY8002PI']
dataE = dataframe['TB8002PIB']
dataF = dataframe['TB8004PI']
dataG = dataframe['MX8004PIB']


def rms(scores):
    return np.sqrt(np.mean(scores**2))
def average(scores):
    return np.mean(scores)

scale = 30
timewindow_D = []
timewindow_E = []
timewindow_F = []
timewindow_G = []


if __name__ == '__main__':
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
    # peaks1, _ = find_peaks(timewindow_D, height=0.01, distance = 500, width=1)
    # peaks2, _ = find_peaks(timewindow_E, height=0.01, distance = 500, width=1)
    # peaks3, _ = find_peaks(timewindow_F, height=0.01, distance = 500, width=1)
    # peaks4, _ = find_peaks(timewindow_G, height=0.01, distance = 500, width=1)
    # peaks5, _ = find_peaks(timewindow_delta_D, distance = 500)
    # peaks6, _ = find_peaks(timewindow_delta_E, distance = 500)
    # peaks7, _ = find_peaks(timewindow_delta_F, distance = 500)
    # peaks8, _ = find_peaks(timewindow_delta_G, distance = 500)
    peaks9, peaks91 = find_peaks(delta_D_scale, height=0.03,  width=1.5)
    peaks10, peaks101 = find_peaks(delta_E_scale, height=0.03, width=1.5)
    peaks11, _ = find_peaks(delta_F_scale, height=0.03,width=1.5)
    peaks12, _ = find_peaks(delta_G_scale, height=0.03,width=1.5)


    print("------")
    print("--0.91: ",type(peaks9),len(peaks9), peaks9)
    print("--0.92: ",type(peaks91),len(peaks91))
    print("------")
    print("--0.93: ",type(peaks10),len(peaks10), peaks10)
    print("--0.94: ",type(peaks101),len(peaks101))
    print("------")
    print("--0.95: ",type(peaks11),len(peaks11), peaks11)
    print("------")
    print("--0.96: ",type(peaks12),len(peaks12), peaks11)
    print("------")
    # for k,v in peaks91.items():
    #     print(k,v)
    #=================================================================
    # print("------")
    # fig,axes = plt.subplots(4, 2, figsize=(21,14) )
    # axes[0,0].plot(timewindow_D)
    # # axes[0,0].plot(peaks1, timewindow_D[peaks1],"xr")
    # axes[0,0].set_title('XY8002PI', fontsize=13)
    # axes[1,0].plot(timewindow_E)
    # # axes[1,0].plot(peaks2, timewindow_E[peaks2],"xr")
    # axes[1,0].set_title('TB8002PIB', fontsize=13)
    # axes[2,0].plot(timewindow_F)
    # # axes[2,0].plot(peaks3, timewindow_F[peaks3],"xr")
    # axes[2,0].set_title('TB8004PI', fontsize=13)
    # axes[3,0].plot(timewindow_G)
    # # axes[3,0].plot(peaks4, timewindow_G[peaks4],"xr")
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
    #
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
    time = []
    if getpeaktime1.shape[0] <= 0 and getpeaktime2.shape[0] <= 0:
        print('=== normal ===')
    else:
        print('=== abnormal ===')
        for i in getpeaktime1:

            print("--3: ",i,type(getpeaktime1))

            time.append(dataframe.iloc[i, 0])
        print("--3.1: ",dataframe.iloc[0, 0])
        print("--3.2: ",dataframe.iloc[1, 0])
        print("--3.3: ",dataframe.iloc[2, 0])
        print("--3.4: ",dataframe.iloc[3, 0])
        for i in getpeaktime2:

            print("--4: ",i,dataframe.iloc[i, 0])

            time.append(dataframe.iloc[i, 0])
        time.sort()
        for i in time:
            print(i)
            path = 'output.txt'
            f = open(path, 'a')
            f.write(i+'\n')
            f.close()

    """
    2021-06-30 11:00:03
    2021-06-30 11:01:38
    2021-06-30 11:09:49
    2021-06-30 11:16:57
    """