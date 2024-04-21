import os
import subprocess as sp
import numpy as np
import shutil
import random
import matplotlib.pyplot as plt
import scipy.stats
from datetime import datetime

import constants


def meanConfidenceInterval(data: list[float], confidence=0.95) -> tuple[float, float]:
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m-h, m+h


def writeCheckResult(inputMatrix: list[list[int]], matrixSize: int, threadsNum: int):
    matrix4Check = []
    readMatrix(
        f'data/{matrixSize}/{threadsNum}_threads/matrixRes.txt', matrixSize, matrix4Check)

    print(f"READ matrix4Check size={matrixSize}")

    matrix4Check = np.array(matrix4Check).tolist()[0]
    convertInputMatrix = []
    for elem in np.array(inputMatrix).tolist():
        convertInputMatrix.append(elem[0])

    correct = np.array_equal(matrix4Check, convertInputMatrix)

    with open(f"data/{matrixSize}/{matrixSize}_checkResult.txt", "a", encoding='utf-8') as file:
        file.write(
            f"Matrix size: {matrixSize} Threads number: {threadsNum} Correct: {correct}\n")
    print(f'Threads num: {threadsNum}\nCheck: {correct}')


def readMatrix(fileName: str, matrixSize: int, matrixDest: list[int]) -> None:
    help = []
    mat = np.genfromtxt(fileName, dtype=int).tolist()

    for i in mat:
        help.append(i)
        if len(help) == matrixSize:
            matrixDest.append(help.copy())
            help.clear()


def runMulMatrix(fileName: str, matrixSize: int, threadNumber: int) -> None:
    print(
        f"===START {matrixSize} size with {threadNumber} threads==="
    )

    if sp.run(f"{fileName} {matrixSize} {threadNumber}").returncode == 0:
        print(
            f"===FINISH {matrixSize} size with {threadNumber} threads===\n\n"
        )


def createData(filename: str, matrixSize: int) -> None:
    random.seed()
    with open(filename, "w+", encoding="utf-8") as file:
        for i in range(matrixSize):
            for j in range(matrixSize):
                file.write(f'{random.randint(0, 10)} ')
            file.write('\n')


if __name__ == "__main__":
    os.system('cls')

    t1 = datetime.strptime(
        f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}', "%H:%M:%S")
    print('Start time:', t1.time())

    if os.path.isdir('data'):
        shutil.rmtree('data')
    os.mkdir('data')

    # /////////////////////////////////////////////
    # /////////////// CREATE DATA /////////////////
    # /////////////////////////////////////////////

    for fName in constants.FILE_NAMES:
        for size in constants.MATRIX_SIZE:
            if not os.path.isdir(f'data/{size}'):
                os.mkdir(f'data/{size}')
            createData(f"data/{size}/{fName}.txt", size)
            if not os.path.isdir(f'data/{size}/1_threads'):
                os.mkdir(f'data/{size}/1_threads')
            print(f"====CREATE {size}/{fName}====")
        print('\n')

    for size in constants.MATRIX_SIZE:
        for th in constants.THREADS_NUMBER:
            if not os.path.isdir(f'data/{size}/{th}_threads'):
                os.mkdir(f'data/{size}/{th}_threads')

    # /////////////////////////////////////////////
    # /////////////// RUN C++ /////////////////////
    # /////////////////////////////////////////////

    for th in constants.THREADS_NUMBER:
        for size in constants.MATRIX_SIZE:
            runMulMatrix(constants.EXE_ABS_PATH, size, th)

    # /////////////////////////////////////////////
    # ////////////// CHECK RESULT /////////////////
    # /////////////////////////////////////////////

    print('\n\n===START CHECK===\n')

    for size in constants.MATRIX_SIZE:
        matrixA = []
        matrixB = []
        matrixRes = []
        readMatrix(f'data/{size}/{constants.FILE_NAMES[0]}.txt', size, matrixA)
        print(f"READ matrixA size={size}")
        readMatrix(f'data/{size}/{constants.FILE_NAMES[1]}.txt', size, matrixB)
        print(f"READ matrixB size={size}")

        print("\n=========================\n")

        matrixRes = np.dot(matrixA, matrixB)[0]
        for th in constants.THREADS_NUMBER:
            writeCheckResult(matrixRes, size, th)
            print("\n=========================\n")

    print('===END CHECK===\n')

    # /////////////////////////////////////////////
    # //////// BUILD CONFIDENCE INTERVAL //////////
    # /////////////////////////////////////////////

    print('===START BUILD CONFIDENCE INTERVAL===\n')

    allTime = []
    allCIntervals = [[] for i in range(len(constants.MATRIX_SIZE))]
    for th in constants.THREADS_NUMBER:
        temp = []
        for size in constants.MATRIX_SIZE:
            vedro = []
            with open(f'data/{size}/{th}_threads/result.txt', "r", encoding="utf-8") as file:
                for time in file.read().split('Time: ')[1].split(" "):
                    if time != "\n":
                        vedro.append(float(time))
            temp.append(vedro)
        allTime.append(temp)

    index = 0

    for times in allTime:
        print(
            f"\nConfidence interval for threads number {constants.THREADS_NUMBER[index]}")
        for t, j in zip(times, range(len(times))):
            interval = meanConfidenceInterval(t)
            print(f"Size {constants.MATRIX_SIZE[j]}: {interval}")
            allCIntervals[j].append(interval)

        index += 1

    for inter, i in zip(allCIntervals, range(len(constants.MATRIX_SIZE))):
        for th, j in zip(constants.THREADS_NUMBER, range(len(constants.THREADS_NUMBER))):
            with open(f"data/{constants.MATRIX_SIZE[i]}/CInterval.txt", "a", encoding="utf-8") as file:
                file.write(f"Threads number: {th} => {inter[j]}\n")

    print('\n\n===END BUILD CONFIDENCE INTERVAL===\n')

    # /////////////////////////////////////////////
    # ///////////// CREATE DIAGRAM ////////////////
    # /////////////////////////////////////////////

    print('===START CREATE DIAGRAM===\n')

    allMeanTimes = [[] for i in range(len(constants.THREADS_NUMBER))]

    for time, index in zip(allTime, range(len(constants.THREADS_NUMBER))):
        for t in time:
            allMeanTimes[index].append(np.mean(t))

    for meanTime, index in zip(allMeanTimes, range(len(allMeanTimes))):
        plt.errorbar(constants.MATRIX_SIZE, meanTime,
                     label=f"{constants.THREADS_NUMBER[index]} threads")
        plt.xlabel("size")
        plt.ylabel("time(s)")
    plt.legend()
    plt.savefig("img.png")
    print('Show diagram\n')
    print('===END CREATE DIAGRAM===\n')

    t2 = datetime.strptime(
        f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}', "%H:%M:%S")
    print('End time:', t2.time())

    delta = t2 - t1

    print(f"Complited in {delta.total_seconds() / 60} minutes")
