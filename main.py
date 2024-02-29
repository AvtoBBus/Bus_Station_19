import os
import subprocess as sp
import numpy as np
import shutil
import matplotlib.pyplot as plt

import generate_report as gr


def read_time(path_to_file: str) -> list[float]:
    times = []
    with open(path_to_file, "r", encoding="utf-8") as file:
        for line in file.readlines():
            times.append(float(line.split("Time: ")[1]))
    return times


def generate_matrix(path_to_exe: str, matrix_size: int) -> None:
    print(f"===START {matrix_size} size===")
    if sp.run(f"{path_to_exe} {matrix_size}").returncode == 0:
        print(f"===FINISH {matrix_size} size===\n\n")


def read_matrix(file_name: str, matrix_destination: list[int], size: int) -> None:

    help = []
    mat = np.genfromtxt(file_name, dtype=int).tolist()

    for i in mat:
        help.append(i)
        if len(help) == size:
            matrix_destination.append(help.copy())
            help.clear()


def mul_matrix_func(mat1: list[list[int]], mat2: list[list[int]]) -> list[list[int]]:
    return np.dot(mat1, mat2)


def main(path_to_exe: str, matrix_size: int, files: list[str]) -> bool:
    generate_matrix(path_to_exe, matrix_size)

    matrix1 = []
    matrix2 = []
    matrix_result = []

    read_matrix(f"{matrix_size}/{files[0]}", matrix1, matrix_size)
    read_matrix(f"{matrix_size}/{files[1]}", matrix2, matrix_size)
    read_matrix(f"{matrix_size}/{files[2]}", matrix_result, matrix_size)

    matrix1 = matrix1[0]
    matrix2 = matrix2[0]
    matrix_result = matrix_result[0]

    matrix_mul = mul_matrix_func(matrix1, matrix2)

    return np.array_equal(matrix_mul, matrix_result)


if __name__ == "__main__":
    ABS_PATH = "D:/учёба/для себя/Bus_Station_19/Lab1/x64/Debug/Lab1.exe"
    MATRIX_SIZES = [10, 100, 500, 700, 1000, 1500, 2000]
    result_compare = []
    FILES_NAMES = [
        "Matrix_1.txt",
        "Matrix_2.txt",
        "Matrix_res.txt",
        "Result.txt"
    ]

    os.system('cls')

    os.remove("Result.txt")
    for size in MATRIX_SIZES:
        if os.path.isdir(str(size)):
            shutil.rmtree(str(size))
        os.mkdir(str(size))
        result_compare.append(main(ABS_PATH, size, FILES_NAMES))

    COMP_RES_PATH = "Compare result.txt"

    if os.path.isfile(COMP_RES_PATH):
        os.remove(COMP_RES_PATH)

    for i in range(len(MATRIX_SIZES)):
        with open(COMP_RES_PATH, "a", encoding="utf-8") as file:
            file.write(
                f'Result with {MATRIX_SIZES[i]} -> {"Equal" if result_compare[i] else "NOT equal"}\n'
            )
    print("Finish create result")

    list_times = read_time("Result.txt")

    plt.plot(list_times, MATRIX_SIZES)
    plt.xlabel("time(s)")
    plt.ylabel("size")
    plt.savefig("img.png")

    gr.generate_report()
