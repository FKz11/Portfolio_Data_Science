"""
Реализовать сложение и перемножение произвольных матриц.
Реализовать вычисления определителя произвольной матрицы: разложение по первой строке,
приведение к верхнетреугольному виду.
Реализовать нахождение обратной матрицы: с помощью матрицы дополнений, с помощью единичной матрицы(метод Гаусса).
Реализовать алгоритмы решения СЛАУ: метод Крамера, метод Гаусса, метод LU-разложения.
"""


def enter_n_lines_m_columns(line):
    data = input(line)
    if data.isdigit():
        if int(data) != 0:
            return int(data)
    print("Invalid input!!!")
    return enter_n_lines_m_columns(line)


def enter_vector(line, length):
    try:
        data: list = input(line).split(" ")
        assert len(data) == length
        for i in range(length):
            if "." in list(data[i]):
                data[i] = float(data[i])
            else:
                data[i] = int(data[i])
        return data
    except (AssertionError, ValueError):
        print("Invalid input!!!")
        return enter_vector(line, length)


def enter_array(line, n_lines, m_columns):
    print(line)
    array = []
    try:
        for _ in range(n_lines):
            data: list = input().split(" ")
            assert len(data) == m_columns
            for i in range(m_columns):
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
    def copy_array(cls, array):
        n_lines = len(array)
        m_columns = len(array[0])
        new_array = [[0 for _ in range(m_columns)] for _ in range(n_lines)]
        for i in range(n_lines):
            for j in range(m_columns):
                new_array[i][j] = array[i][j]
        return new_array

    @classmethod
    def one_array(cls, number):
        return [[1 if i == j else 0 for j in range(number)] for i in range(number)]

    @classmethod
    def transpose(cls, matrix):
        new_array = [[matrix.array[i][j] for i in range(matrix.n_lines)] for j in range(matrix.m_columns)]
        new_matrix = cls(new_array, matrix.m_columns, matrix.n_lines)
        return new_matrix

    @classmethod
    def sum(cls, matrix1, matrix2):
        if (matrix1.n_lines != matrix2.n_lines) or (matrix1.m_columns != matrix2.m_columns):
            print("ERROR: (matrix1.n_lines != matrix2.n_lines) or (matrix1.m_columns != matrix2.m_columns)")
            return None
        new_array = [[matrix1.array[i][j] + matrix2.array[i][j] for j in range(matrix1.m_columns)] for i in
                     range(matrix1.n_lines)]
        new_matrix = cls(new_array, matrix1.n_lines, matrix1.m_columns)
        return new_matrix

    @classmethod
    def dot(cls, matrix1, matrix2):
        if matrix1.m_columns != matrix2.n_lines:
            print("ERROR: matrix1.m_columns != matrix2.n_lines")
            return None
        new_array = [[0 for _ in range(matrix2.m_columns)] for _ in range(matrix1.n_lines)]
        for i in range(matrix1.n_lines):
            for j in range(matrix2.m_columns):
                new_array[i][j] = sum([matrix1.array[i][k] * matrix2.array[k][j] for k in range(matrix1.m_columns)])
        new_matrix = cls(new_array, matrix1.n_lines, matrix2.m_columns)
        return new_matrix

    @classmethod
    def det_decomposition(cls, array):
        if len(array[0]) == 1:
            return array[0][0]
        det = 0
        for k in range(len(array[0])):
            det += ((-1) ** k) * array[0][k] * cls.det_decomposition(
                [[array[i][j] for j in range(len(array[0])) if j != k] for i in range(1, len(array))])
        return det

    @classmethod
    def det_upper_triangular(cls, origin_array):
        array: list = cls.copy_array(origin_array)
        length = len(array)
        sign = 0
        for j in range(length - 1):
            if array[j][j] == 0:
                for i in range(j + 1, length):
                    if array[i][j] != 0:
                        array[i], array[j] = array[j], array[i]
                        sign += 1
                        break
            for i in range(j + 1, length):
                if array[i][j] != 0:
                    array[i] = [x - y for x, y in zip(array[i], [k * (array[i][j] / array[j][j]) for k in array[j]])]
        det = (-1) ** sign
        for i in range(length):
            det *= array[i][i]
        return det

    @classmethod
    def det(cls, matrix):
        if matrix.n_lines != matrix.m_columns:
            print("ERROR: matrix.n_lines != matrix.m_columns")
            return None
        return {"Decomposition by the first line": round(cls.det_decomposition(matrix.array), cls.class_round),
                "Bringing to the upper-triangular form": round(cls.det_upper_triangular(matrix.array), cls.class_round)}

    @classmethod
    def inv_addition(cls, matrix):
        a_det = cls.det_upper_triangular(matrix.array)
        if matrix.n_lines == 1:
            return cls([[1 / a_det]], matrix.n_lines, matrix.m_columns)
        new_array = cls.copy_array(matrix.array)
        for i in range(matrix.n_lines):
            for j in range(matrix.m_columns):
                new_array[i][j] = ((-1) ** (i + j)) * cls.det_upper_triangular(
                    [[matrix.array[q][w] for w in range(matrix.m_columns) if w != j] for q in range(matrix.n_lines) if
                     q != i]) / a_det
        new_matrix = cls.transpose(cls(new_array, matrix.n_lines, matrix.m_columns))
        return new_matrix

    @classmethod
    def inv_one(cls, matrix):
        one_array = cls.one_array(matrix.n_lines)
        new_array = cls.copy_array(matrix.array)
        for i in range(matrix.n_lines):
            new_array[i] += one_array[i]
        for i in range(matrix.n_lines):
            if new_array[i][i] == 0:
                for k in range(i + 1, matrix.n_lines):
                    if new_array[k][i] != 0:
                        new_array[i], new_array[k] = new_array[k], new_array[i]
                        break
            for j in range(2 * matrix.m_columns - 1, i - 1, -1):
                new_array[i][j] /= new_array[i][i]
            for k in range(matrix.n_lines):
                if k != i:
                    new_array[k] = [new_array[k][j] - new_array[i][j] * new_array[k][i] for j in
                                    range(2 * matrix.m_columns)]
        new_matrix = cls([new_array[i][matrix.m_columns:] for i in range(matrix.n_lines)], matrix.n_lines,
                         matrix.m_columns)
        return new_matrix

    @classmethod
    def inv(cls, matrix):
        if matrix.n_lines != matrix.m_columns:
            print("ERROR: matrix.n_lines != matrix.m_columns")
            return None
        if cls.det_upper_triangular(matrix.array) == 0:
            print("ERROR: det == 0")
            return None
        return {"inv_addition": cls.inv_addition(matrix),
                "inv_one": cls.inv_one(matrix)}

    @classmethod
    def kramer(cls, array, vector):
        a_det = cls.det_upper_triangular(array)
        length = len(vector)
        x = dict()
        for k in range(length):
            x["x" + str(k + 1)] = cls.det_upper_triangular(
                [array[i][:k] + [vector[i]] + array[i][k + 1:] for i in range(length)]) / a_det
        return x

    @classmethod
    def gauss(cls, origin_array, vector):
        array: list = cls.copy_array(origin_array)
        length = len(vector)
        for i in range(length):
            array[i].append(vector[i])
        for j in range(length - 1):
            if array[j][j] == 0:
                for i in range(j + 1, length):
                    if array[i][j] != 0:
                        array[i], array[j] = array[j], array[i]
                        break
            for i in range(j + 1, length):
                if array[i][j] != 0:
                    c = array[i][j] / array[j][j]
                    array[i] = [x - y for x, y in zip(array[i], [k * c for k in array[j]])]
        x = dict()
        for i in range(length - 1, -1, -1):
            x["x" + str(i + 1)] = (array[i][length] - sum(
                [array[i][k] * x["x" + str(k + 1)] for k in range(i + 1, length)])) / array[i][i]
        return x

    @classmethod
    def lu_decomposition_array(cls, origin_array):
        u_array: list = cls.copy_array(origin_array)
        length = len(origin_array)
        l_array = [[0 if i != j else 1 for j in range(length)] for i in range(length)]
        pilot = list(range(length))
        for j in range(length - 1):
            if u_array[j][j] == 0:
                for i in range(j + 1, length):
                    if u_array[i][j] != 0:
                        u_array[i], u_array[j] = u_array[j], u_array[i]
                        l_array[i][:j], l_array[j][:j] = l_array[j][:j], l_array[i][:j]
                        pilot[j], pilot[i] = pilot[i], pilot[j]
                        break
            for i in range(j + 1, length):
                if u_array[i][j] != 0:
                    c = u_array[i][j] / u_array[j][j]
                    u_array[i] = [x - y for x, y in zip(u_array[i], [k * c for k in u_array[j]])]
                    l_array[i][j] = c
        return {"u_array": u_array, "l_array": l_array, "pilot": pilot}

    @classmethod
    def lu_decomposition_vector(cls, u_array, l_array, pilot, origin_vector):
        length = len(origin_vector)
        vector = [origin_vector[i] for i in pilot]
        y = list()
        for i in range(length):
            y.append((vector[i] - sum([l_array[i][k] * y[k] for k in range(i)])) / l_array[i][i])
        x = dict()
        for i in range(length - 1, -1, -1):
            x["x" + str(i + 1)] = (y[i] - sum(
                [u_array[i][k] * x["x" + str(k + 1)] for k in range(i + 1, length)])) / u_array[i][i]
        return x

    @classmethod
    def lu_decomposition(cls, origin_array, origin_vector):
        return cls.lu_decomposition_vector(**cls.lu_decomposition_array(origin_array), origin_vector=origin_vector)

    @classmethod
    def solution(cls, matrix, vector):
        if matrix.n_lines != matrix.m_columns:
            print("ERROR: matrix.n_lines != matrix.m_columns")
            return None
        a_det = cls.det_upper_triangular(matrix.array)
        if a_det == 0:
            print("ERROR: a_det == 0")
            return None
        return {"Kramer's method": {y: round(x, cls.class_round) for y, x in cls.kramer(matrix.array, vector).items()},
                "The Gauss method": {y: round(x, cls.class_round) for y, x in
                                     reversed(cls.gauss(matrix.array, vector).items())},
                "LU-decomposition method": {y: round(x, cls.class_round) for y, x in
                                            reversed(cls.lu_decomposition(matrix.array, vector).items())}}

    def __str__(self):
        data = ""
        for line in self.array:
            for k in line:
                data += str(round(k, self.class_round)) + " "
            data += "\n"
        return data[:-1]


if __name__ == "__main__":
    print("Enter the matrices A and B to add, multiply, find their determinants and inverse matrices")
    A_n_lines = enter_n_lines_m_columns("Enter the number of lines of the matrix A\n>>>:")
    A_m_columns = enter_n_lines_m_columns("Enter the number of columns of matrix A\n>>>:")
    A_array = enter_array("Enter the values in the line of the matrix A separated by a space,"
                          " to move to the next line, press enter\n>>>:", A_n_lines, A_m_columns)
    B_n_lines = enter_n_lines_m_columns("Enter the number of lines of the matrix B\n>>>:")
    B_m_columns = enter_n_lines_m_columns("Enter the number of columns of matrix B\n>>>:")
    B_array = enter_array("Enter the values in the line of the matrix B separated by a space,"
                          " to move to the next line, press enter\n>>>:", B_n_lines, B_m_columns)
    print("Enter a system of linear equations in the form of a matrix C and a vector of values V to find solutions")
    C_n_lines = enter_n_lines_m_columns("Enter the number of lines of the matrix C\n>>>:")
    C_m_columns = enter_n_lines_m_columns("Enter the number of columns of matrix C\n>>>:")
    C_array = enter_array("Enter the values in the line of the matrix C separated by a space,"
                          " to move to the next line, press enter\n>>>:", C_n_lines, C_m_columns)
    V_vector = enter_vector("Enter the vector of values V separated by a space\n>>>:\n", C_n_lines)
    A_matrix = Matrix(A_array, A_n_lines, A_m_columns)
    B_matrix = Matrix(B_array, B_n_lines, B_m_columns)
    C_matrix = Matrix(C_array, C_n_lines, C_m_columns)
    print("------------------------------------------")
    print(f"A+B and B+A:\n{Matrix.sum(A_matrix, B_matrix)}\n")
    print(f"A*B:\n{Matrix.dot(A_matrix, B_matrix)}\n")
    print(f"B*A:\n{Matrix.dot(B_matrix, A_matrix)}\n")
    print(f"Determinant A:\n{Matrix.det(A_matrix)}\n")
    print(f"Determinant B:\n{Matrix.det(B_matrix)}\n")
    print(f"The inverse matrix A:")
    A_inv = Matrix.inv(A_matrix)
    if A_inv is not None:
        print(f"Using the matrix of additions:\n{A_inv['inv_addition']}"
              f"\nUsing the unit matrix(Gauss method):\n{A_inv['inv_one']}\n")
    else:
        print(f"{None}\n")
    print(f"The inverse matrix B:")
    B_inv = Matrix.inv(B_matrix)
    if B_inv is not None:
        print(f"Using the matrix of additions:\n{B_inv['inv_addition']}"
              f"\nUsing the unit matrix(Gauss method):\n{B_inv['inv_one']}\n")
    else:
        print(f"{None}\n")
    print(f'Solution of a system of linear equations given by a matrix C '
          f'and a vector of values V:\n{Matrix.solution(C_matrix, V_vector)}\n')
