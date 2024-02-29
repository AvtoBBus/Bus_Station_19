#include <fstream>
#include <vector>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <stdio.h>
#include <string>
#include <sstream>
#include <stdlib.h>


using namespace std;


void create_file_matrix(string file_name, const vector<vector<int>>& matrix)
{
    ofstream out;
    out.open(file_name);
    if (out.is_open())
    {
        for (int i = 0; i < matrix.size(); i++)
        {
            for (int j = 0; j < matrix.size(); j++)
            {
                out << " " << matrix[i][j];
            }
            out << endl;
        }
    }
    out.close();
}

void create_matrix(string file_name, int size)
{
    vector<vector<int>> m(size, vector<int>(size));

    for (int i = 0; i < m.size(); i++)
    {
        for (int j = 0; j < m.size(); j++)
        {
            m[i][j] = rand() % 500;
        }
    }
    create_file_matrix(file_name, m);
}

void read_matrix(vector<vector<int>>& matrix, int size, string file_name)
{
    ifstream data;
    data.open(file_name);

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

}

void mul_matrix(const vector<vector<int>>& matrix_1, const vector<vector<int>>& matrix_2, vector<vector<int>>& matrix_result)
{
    for (int i = 0; i < matrix_result.size(); i++)
    {
        for (int j = 0; j < matrix_result[i].size(); j++)
        {
            matrix_result[i][j] = 0;
            for (int k = 0; k < matrix_2.size(); k++)
            {
                matrix_result[i][j] += matrix_1[i][k] * matrix_2[k][j];
            }

        }
    }
}
void write_result(string str, vector<vector<int>>& matrix_result, int size, clock_t end, clock_t start)
{
    ofstream data(str);
    ofstream result("Result.txt", ios::app);


    for (int i = 0; i < matrix_result.size(); i++)
    {
        for (int j = 0; j < matrix_result[i].size(); j++)
        {
            data << " " << matrix_result[i][j];
        }
        data << endl;
    }

    result << "Size: " << size << " Time: " << (double(end - start)) / (double(CLOCKS_PER_SEC)) << endl;
    data.close();
    result.close();
}

int main(int argc, char* argv[])
{
    // D:\учёба\для себя\Bus_Station_19\Lab1\x64\Debug
    srand(time(NULL));
    const int SIZE = atoi((const char*)argv[1]);
    vector<vector<int>> matrix_1(SIZE, vector<int>(SIZE));
    vector<vector<int>> matrix_2(SIZE, vector<int>(SIZE));
    vector<vector<int>> matrix_result(SIZE, vector<int>(SIZE));


    stringstream ss;

    ss << to_string(SIZE);
    ss << "/Matrix_1.txt";

    string m1_filename = ss.str();

    ss.str("");
    

    ss << to_string(SIZE);
    ss << "/Matrix_2.txt";

    string m2_filename = ss.str();

    ss.str("");


    ss << to_string(SIZE);
    ss << "/Matrix_res.txt";

    string mRes_filename = ss.str();

    ss.str("");

    cout << m1_filename << endl << m2_filename << endl << mRes_filename << endl;


    create_matrix(m1_filename, SIZE);
    create_matrix(m2_filename, SIZE);
    read_matrix(matrix_1, SIZE, m1_filename);
    read_matrix(matrix_2, SIZE, m2_filename);

    clock_t start, end;
    start = clock();
    mul_matrix(matrix_1, matrix_2, matrix_result);
    end = clock();


    write_result(mRes_filename, matrix_result, SIZE, end, start);

    return 0;

}