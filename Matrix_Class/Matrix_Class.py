"""
Реализовать перемножение произвольных матриц.
Реализовать вычисление определителя произвольной матрицы.
"""


def enter_n_lines_m_columns(line):
    data = input(line)
    if data.isdigit():
        if int(data) != 0:
            return int(data)
    print("Invalid input!!!")
    return enter_n_lines_m_columns(line)


def enter_array(line, n_lines, m_columns):
    print(line)
    array = []
    try:
        for _ in range(n_lines):
            data: list = input().split(" ")
            assert len(data) == m_columns
            for i in range(len(data)):
                if "." in list(data[i]):
                    data[i] = float(data[i])
                else:
                    data[i] = int(data[i])
            array.append(data)
        return array
    except (AssertionError, ValueError):
        print("Invalid input!!!")
        return enter_array(line, n_lines, m_columns)


class Matrix:
    class_round = 10

    def __init__(self, array, n_lines, m_columns):
        self.array = array
        self.n_lines = n_lines
        self.m_columns = m_columns

    @classmethod
    def dot(cls, matrix1, matrix2):
        if matrix1.m_columns != matrix2.n_lines:
            print("ERROR: matrix1.m_columns != matrix2.n_lines")
            return None
        else:
            new_array = [[0 for _ in range(matrix2.m_columns)] for _ in range(matrix1.n_lines)]
            for i in range(matrix1.n_lines):
                for j in range(matrix2.m_columns):
                    new_array[i][j] = sum([matrix1.array[i][k] * matrix2.array[k][j] for k in range(matrix1.m_columns)])
            new_matrix = cls(new_array, matrix1.n_lines, matrix2.m_columns)
            return new_matrix

    @classmethod
    def det_array(cls, array):
        if len(array[0]) == 1:
            return array[0][0]
        else:
            det = 0
            for k in range(len(array[0])):
                det += ((-1) ** k) * array[0][k] * \
                       cls.det_array([array[i][:k] + array[i][k + 1:] for i in range(1, len(array[0]))])
            return det

    @classmethod
    def det(cls, matrix):
        if matrix.n_lines != matrix.m_columns:
            print("ERROR: matrix.n_lines != matrix.m_columns")
            return None
        else:
            return round(cls.det_array(matrix.array), cls.class_round)

    def __str__(self):
        data = ""
        for line in self.array:
            for k in line:
                data += str(round(k, self.class_round)) + " "
            data += "\n"
        return data[:-1]


if __name__ == "__main__":
    A_n_lines = enter_n_lines_m_columns("Enter the number of lines of the matrix A\n>>>:")
    A_m_columns = enter_n_lines_m_columns("Enter the number of columns of matrix A\n>>>:")
    A_array = enter_array("Enter the values in the line of the matrix A separated by a space,"
                          " to move to the next line, press enter\n>>>:", A_n_lines, A_m_columns)
    B_n_lines = enter_n_lines_m_columns("Enter the number of lines of the matrix B\n>>>:")
    B_m_columns = enter_n_lines_m_columns("Enter the number of columns of matrix B\n>>>:")
    B_array = enter_array("Enter the values in the line of the matrix B separated by a space,"
                          " to move to the next line, press enter\n>>>:", B_n_lines, B_m_columns)
    A_matrix = Matrix(A_array, A_n_lines, A_m_columns)
    B_matrix = Matrix(B_array, B_n_lines, B_m_columns)
    print("------------------------------------------")
    print(f"A*B:\n{Matrix.dot(A_matrix, B_matrix)}\n")
    print(f"B*A:\n{Matrix.dot(B_matrix, A_matrix)}\n")
    print(f"Determinant A:\n{Matrix.det(A_matrix)}\n")
    print(f"Determinant B:\n{Matrix.det(B_matrix)}\n")
