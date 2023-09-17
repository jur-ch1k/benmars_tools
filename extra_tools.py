import keyboard
import time
import traceback
import sys
import os
import shutil


def waitAndClick():
    # for i in range(3):
    #     for j in range(6):
    time.sleep(30)
    keyboard.send('up')
    keyboard.send('enter')
    # keyboard.send('alt+tab')
    # for j in range(60):
    #     time.sleep(10)
    #     keyboard.send('up')
    #     keyboard.send('enter')
    #     keyboard.send('alt+tab')


def equasion():
    for x in range(1, 5000):
        if 35000 % x == 0:
            print(x)


def getTasksNum():
    cnt = 0
    print(os.listdir('.'))
    with open('./out', 'r') as f:
        lines = f.readlines()
    for line in lines:
        words = line.split()
        for word in words:
            if '1573' in word:
                print(word)
                cnt += 1
    print(cnt)


def transferfiles():
    files = os.listdir('./_scratch')
    for file in files:
        if 'slurm' in file:
            with open('./_scratch/' + file, 'r') as f:
                lines = f.readlines()
            words = lines[46].split()
            nb = words[2]
            p = words[3]
            q = words[4]
            if int(p)*int(q) != 1:
                shutil.move('./_scratch/' + file, './-O228/MPI_Proc_Num=' + str(int(p)*int(q)) + '/Nb=' + nb + '/PxQ=' + p + 'x' + q)
            else:
                shutil.move('./_scratch/' + file, './-O228/MPI_Proc_Num=' + str(int(p) * int(q)) + '/Nb=' + nb)


def speed():
    text = """VM5729:6 640,1
VM5729:6 630,0
VM5729:6 599,0
VM5729:6 590,3
VM5729:6 639,7
VM5729:6 592,3
VM5729:6 NaN
VM5729:6 632,1
VM5729:6 621,9
VM5729:6 640,1
VM5729:6 661,7
VM5729:6 NaN
VM5729:6 624,0
VM5729:6 599,9
VM5729:6 596,9
VM5729:6 545,2
VM5729:6 663,1
VM5729:6 580,2
VM5729:6 666,6
VM5729:6 663,9
VM5729:6 504,7
3VM5729:6 NaN
VM5729:6 953,8
2VM5729:6 NaN
VM5729:6 944,0
2VM5729:6 NaN
VM5729:6 969,8
VM5729:6 958,2
VM5729:6 987,0
VM5729:6 996,1
VM5729:6 982,2
VM5729:6 907,4
VM5729:6 995,1
VM5729:6 922,7
VM5729:6 995,2
VM5729:6 957,2
VM5729:6 1003,2
VM5729:6 1032,7
VM5729:6 998,7
VM5729:6 1034,5
VM5729:6 1010,6
VM5729:6 984,8
VM5729:6 1000,6
VM5729:6 964,8
VM5729:6 1005,6
VM5729:6 980,6
5VM5729:6 NaN"""
    lines = text.split('\n')
    print(len(lines))
    for line in lines:
        if str.isdigit(line.split()[0][0]):
            for i in range(int(line.split()[0][0])):
                print(line.split()[-1])
        else:
            print(line.split()[-1])


def test(matrix):

    lengh = len(matrix[0])
    tmp = [[0 for x in range(lengh)] for y in range(lengh)]

    for i in range(lengh):
        for j in range(lengh):
            tmp[j][-(i + 1)] = matrix[i][j]
        print(tmp)
    del matrix
    matrix = tmp
    return matrix

if __name__ == '__main__':
    print(test([[1,2,3],[4,5,6],[7,8,9]]))
