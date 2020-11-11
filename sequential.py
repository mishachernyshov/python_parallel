import random
import time

class Matrix:
    def __init__(self, rows, cols):
        self.matr = []
        
        for k in range(rows):
            self.matr.append([])
            for n in range(cols):
                self.matr[k].append(round(random.random() * 1000))


def addNumbers(frst_num, scnd_num):
    return frst_num + scnd_num

def substractNumbers(frst_num, scnd_num):
    return frst_num - scnd_num


class MatrixOperations:    
    def elementwiseOperation(self, fist_matr, frst_rows, frst_cols,
                 scnd_matr, scnd_rows, scnd_cols, operation):
        if frst_rows != scnd_rows or frst_cols != scnd_cols:
            print("Матриці мають різні розміри")
            return
        operationFunction = None
        if operation == '+':
            operationFunction = addNumbers
        elif operation == '-':
            operationFunction = substractNumbers
        summed_matrix = \
            [[0 for i in range(frst_cols)] for k in range(frst_rows)]
        for i in range(frst_rows):
            for j in range(scnd_cols):
                summed_matrix[i][j] = \
                    operationFunction(fist_matr.matr[i][j], scnd_matr.matr[i][j])
        return summed_matrix

    def addition(self, fist_matr, frst_rows,
                 frst_cols, scnd_matr, scnd_rows, scnd_cols):
        return self.elementwiseOperation(fist_matr, frst_rows, frst_cols,
                scnd_matr, scnd_rows, scnd_cols, '+')

    def substraction(self, fist_matr, frst_rows,
                 frst_cols, scnd_matr, scnd_rows, scnd_cols):
        return self.elementwiseOperation(fist_matr, frst_rows, frst_cols,
                scnd_matr, scnd_rows, scnd_cols, '-')

def get_time_execution(function, *args):
    start = time.time()
    function(*args)
    return time.time() - start


def evaluateFuncEfficiency(func, times, *args):
    efficiency = float('inf')
    current_eff = None
    for k in range(times):
        current_eff = get_time_execution(func, *args)
        if current_eff < efficiency:
            efficiency = current_eff
    return efficiency


if __name__ == '__main__':
    ROWS = 4000
    COLS = 4000
    TIME_REPETITION = 10

    a = Matrix(ROWS, COLS)
    b = Matrix(ROWS, COLS)

    z = MatrixOperations()

    print('Час додавання матриць:',
          evaluateFuncEfficiency(z.addition, TIME_REPETITION, a, ROWS, COLS, b, ROWS, COLS))
    print('Час віднімання матриць:',
          evaluateFuncEfficiency(z.substraction, TIME_REPETITION, a, ROWS, COLS, b, ROWS, COLS))
