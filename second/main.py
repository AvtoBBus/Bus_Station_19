import os
import subprocess as sp
import numpy as np
import shutil
import random
import matplotlib.pyplot as plt

import constants


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
    if os.path.isdir('data'):
        shutil.rmtree('data')
    os.mkdir('data')

    # /////////////////////////////////////////////
    # /////////////// CREATE DATA /////////////////
    # /////////////////////////////////////////////

    matrixSize = [10, 50, 100, 500, 600, 700, 800, 900, 1000]
    fileNames = ["matrixA", "matrixB"]
    for fName in fileNames:
        for size in matrixSize:
            if not os.path.isdir(f'data/{size}'):
                os.mkdir(f'data/{size}')
            createData(f"data/{size}/{fName}.txt", size)
            if not os.path.isdir(f'data/{size}/1_threads'):
                os.mkdir(f'data/{size}/1_threads')
            print(f"====CREATE {size}/{fName}====")
        print('\n')

    threadsNum = [1]
    for size in matrixSize:
        for th in range(2, 18, 2):
            threadsNum.append(th)
            os.mkdir(f'data/{size}/{th}_threads')

    # /////////////////////////////////////////////
    # /////////////// RUN C++ /////////////////////
    # /////////////////////////////////////////////

    for th in threadsNum:
        for size in matrixSize:
            runMulMatrix(constants.EXE_ABS_PATH, size, th)
