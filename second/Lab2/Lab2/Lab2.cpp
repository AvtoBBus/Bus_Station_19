#include <fstream>
#include <vector>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <stdio.h>
#include <string>
#include <sstream>
#include <stdlib.h>

#include <omp.h>

using namespace std;

void read_matrix(vector<vector<int>>& matrix, int size, string filename, bool firstMatrix = false)
{
    ifstream data;
    data.open(filename);

    if (data.is_open())
    {
        for (int i = 0; i < matrix.size(); i++)
        {
            for (int j = 0; j < matrix.size(); j++)
            {
                data >> matrix[i][j];
            }
        }
    }
    data.close();
    if (firstMatrix)
    {
        cout << "Read matrixA" << endl;
    }
    else 
    {
        cout << "Read matrixB" << endl;
    }
}

double mul_matrix(const vector<vector<int>>& matrix_1, const vector<vector<int>>& matrix_2, vector<vector<int>>& matrix_result)
{

    double wTime = omp_get_wtime();

    int i = 0, j = 0, k = 0;
#pragma omp parallel for shared(matrix_1, matrix_2, matrix_result) private(i, j, k)

    for (i = 0; i < matrix_result.size(); i++)
    {
        for (j = 0; j < matrix_result[i].size(); j++)
        {
            matrix_result[i][j] = 0;
            for (k = 0; k < matrix_2.size(); k++)
            {
                matrix_result[i][j] += matrix_1[i][k] * matrix_2[k][j];
            }

        }
    }
    wTime = omp_get_wtime() - wTime;
    cout << "wtime: " << wTime << endl;
    return wTime;
}

void write_result(string filename, vector<vector<int>>& matrixRes, int size, int threadNum, double wTime)
{
    ofstream data;
    data.open(filename);

    stringstream ss;

    ss.str("");
    ss << "D:/учёба/для себя/Bus_Station_19/second/data/";
    ss << to_string(size);
    ss << "/";
    ss << to_string(threadNum);
    ss << "_threads";
    ss << "/result.txt";

    ofstream result;
    result.open(ss.str());


    for (int i = 0; i < matrixRes.size(); i++)
    {
        for (int j = 0; j < matrixRes[i].size(); j++)
        {
            data << " " << matrixRes[i][j];
        }
        data << endl;
    }

    result << "Size: " << size << " Threads: " << threadNum << " Time: " << wTime << endl;
    data.close();
    result.close();
}

int main(int argc, char* argv[])
{
    setlocale(LC_ALL, "ru");

    const int THREAD_NUM = atoi((const char*)argv[2]);
    const int SIZE = atoi((const char*)argv[1]);

    vector<vector<int>> matrixA(SIZE, vector<int>(SIZE));
    vector<vector<int>> matrixB(SIZE, vector<int>(SIZE));
    vector<vector<int>> matrixRes(SIZE, vector<int>(SIZE));

    stringstream ss;

    ss << "D:/учёба/для себя/Bus_Station_19/second/data/";
    ss << to_string(SIZE);
    ss << "/matrixA.txt";

    string m1_filename = ss.str();

    ss.str("");

    ss << "D:/учёба/для себя/Bus_Station_19/second/data/";
    ss << to_string(SIZE);
    ss << "/matrixB.txt";

    string m2_filename = ss.str();

    ss.str("");

    ss << "D:/учёба/для себя/Bus_Station_19/second/data/";
    ss << to_string(SIZE);
    ss << "/";
    ss << to_string(THREAD_NUM);
    ss << "_threads";
    ss << "/matrixRES.txt";

    string mRes_filename = ss.str();

    ss.str("");

    read_matrix(matrixA, SIZE, m1_filename, true);
    read_matrix(matrixB, SIZE, m2_filename);

    omp_set_num_threads(THREAD_NUM);

    cout << "current thread number: " << omp_get_max_threads() << endl;

    double wTime = mul_matrix(matrixA, matrixB, matrixRes);

    write_result(mRes_filename, matrixRes, SIZE, THREAD_NUM, wTime);

    return 0;

}