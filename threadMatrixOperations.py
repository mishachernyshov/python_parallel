import random
import threading
import time
from sequential import get_time_execution, evaluateFuncEfficiency


class Matrix:
    def __init__(self, rows, cols, thread_count):
        self.matr = []
        self.rows = rows
        self.cols = cols

        for k in range(rows):
            self.matr.append([])

        appointed_thread_count = None
        thread_coefficients = None
        current_start_value = 0

        if rows <= thread_count:
            appointed_thread_count = rows
            thread_coefficients = [1] * rows
        else:
            appointed_thread_count = thread_count
            thread_coefficients = \
                [rows // thread_count] * thread_count
            for k in range(rows % thread_count):
                thread_coefficients[k] += 1

        thread_list = []

        for k in range(appointed_thread_count):
            current_thread = threading.Thread(target=
                self.initialize, args=(thread_coefficients[k],
                current_start_value))
            current_start_value += thread_coefficients[k]
            thread_list.append(current_thread)
            current_thread.start()

        for k in range(appointed_thread_count):
            thread_list[k].join()

    def initialize(self, col_count, start):
        for k in range(col_count):
            for n in range(self.cols):
                self.matr[start + k].append(round(random.random() * 1000))


def addNumbers(frst_num, scnd_num):
    return frst_num + scnd_num


def substractNumbers(frst_num, scnd_num):
    return frst_num - scnd_num


class MatrixOperations:
    def __init__(self, thread_count):
        self.thread_count = thread_count

    def thread_work(self, col_count, start, col_number,
                    operationFunc, res_matrix, frst_matrix, scnd_matrix):
        for k in range(col_count):
            for n in range(col_number):
                res_matrix[start + k][n] = \
                    operationFunc(frst_matrix.matr[start + k][n],
                                  scnd_matrix.matr[start + k][n])

    def elementwiseOperation(self, fist_matr, frst_rows, frst_cols,
                             scnd_matr, scnd_rows, scnd_cols, operation):
        if frst_rows != scnd_rows or frst_cols != scnd_cols:
            print("Матриці мають різні розміри")
            return

        appointed_thread_count = None
        thread_coefficients = None
        current_start_value = 0

        if frst_rows <= self.thread_count:
            appointed_thread_count = frst_rows
            thread_coefficients = [1] * frst_rows
        else:
            appointed_thread_count = self.thread_count
            thread_coefficients = \
                [frst_rows // self.thread_count] * self.thread_count
            for k in range(frst_rows % self.thread_count):
                thread_coefficients[k] += 1

        operationFunction = None
        if operation == '+':
            operationFunction = addNumbers
        elif operation == '-':
            operationFunction = substractNumbers
        summed_matrix = \
            [[0 for i in range(frst_cols)] for k in range(frst_rows)]

        thread_list = []

        for k in range(appointed_thread_count):
            current_thread = threading.Thread(target=self.thread_work,
                args=(thread_coefficients[k], current_start_value,
                frst_cols, operationFunction, summed_matrix, fist_matr, scnd_matr))
            current_start_value += thread_coefficients[k]
            thread_list.append(current_thread)
            current_thread.start()

        for k in range(appointed_thread_count):
            thread_list[k].join()

        return summed_matrix

    def addition(self, fist_matr, frst_rows,
                 frst_cols, scnd_matr, scnd_rows, scnd_cols):
        return self.elementwiseOperation(fist_matr, frst_rows, frst_cols,
                                         scnd_matr, scnd_rows, scnd_cols, '+')

    def substraction(self, fist_matr, frst_rows,
                     frst_cols, scnd_matr, scnd_rows, scnd_cols):
        return self.elementwiseOperation(fist_matr, frst_rows, frst_cols,
                                         scnd_matr, scnd_rows, scnd_cols, '-')


ROWS = 4000
COLS = 4000
TIME_REPETITION = 10
THREADS = 6

a = Matrix(ROWS, COLS, THREADS)
b = Matrix(ROWS, COLS, THREADS)

z = MatrixOperations(THREADS)

print('Час додавання матриць:',
      evaluateFuncEfficiency(z.addition, TIME_REPETITION, a, ROWS, COLS, b, ROWS, COLS))
print('Час віднімання матриць:',
      evaluateFuncEfficiency(z.substraction, TIME_REPETITION, a, ROWS, COLS, b, ROWS, COLS))
