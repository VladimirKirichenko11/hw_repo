class Matrix:
    # Инициализация матрицы
    def __init__(self, rows=0, cols=0):
        self.rows = rows
        self.cols = cols
        self.data = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(0.0)
            self.data.append(row)

    # Создание матрицы из списков
    def create_from_list(self, data_list):
        self.rows = len(data_list)
        if self.rows > 0:
            self.cols = len(data_list[0])
        else:
            self.cols = 0
        self.data = data_list
        return self

    # Вывод матрицы
    def print_matrix(self):
        print(f"Матрица {self.rows}x{self.cols}:")
        for i in range(self.rows):
            for j in range(self.cols):
                print(f"{self.data[i][j]: 8.2f}", end=" ")
            print()
        print()

    # Установка значений матрицы
    def set_value(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.data[row][col] = float(value)
            return True
        else:
            print(f"Ошибка: позиция ({row}, {col}) вне границы матрицы")
            return False

    # Получение значений из матрицы
    def get_value(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data[row][col]
        else:
            print(f"Ошибка позиция ({row}, {col}) вне границы матрицы")
            return None

    # Сохранение матрицы в файл формата MTX


def save_to_mtx(matrix, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("%%MatrixMarket matrix array real general\n")
            file.write(f"{matrix.rows}, {matrix.cols}")
            # Записываем данные построчно
            for i in range(matrix.rows):
                for j in range(matrix.cols):
                    file.write(f"{matrix.data[i][j]:.6f}\n")
        print(f"Матрица сохранена в файл: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False

    # Загрузка матрицы из формата MTX


def load_from_mtx(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
        # Пропускаем комментарии
        data_lines = []
        for line in lines:
            if not line.strip().startswith("%"):
                data_lines.append(line.strip())
        if len(data_lines) < 2:
            print("Ошибка: неверный формат файла")
            return None
        sizes_line = data_lines[0].replace(",", ".").replace(";", " ")
        sizes = sizes_line.split()
        if len(sizes) != 2:
            print("Ошибка: неверный формат размеров матрицы")
            return None
        rows = int(sizes[0])
        cols = int(sizes[1])
        # Создаем матрицу
        matrix = Matrix(rows, cols)
        if len(data_lines) - 1 != rows * cols:
            print("Ошибка: количество данных не соответствует размеру матрицы")
            return None
        # Заполняем матрицу
        index = 1
        for i in range(rows):
            for j in range(cols):
                if index < len(data_lines):
                    value = float(data_lines[index])
                    matrix.set_value(i, j, value)
                    index += 1
        print(f"Матрица загружена из файла: {filename}")
        return matrix
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке файла {e}")
        return None


def main():
    # Создаём тестовую матрицу 3x3
    matrix1 = Matrix(3, 3)
    value = 1.0
    for i in range(3):
        for j in range(3):
            matrix1.set_value(i, j, value)
            value += 1.0
    matrix1.print_matrix()
    # Сохраняем матрицу в файл
    save_to_mtx(matrix1, "matrix.mtx")
    # Загружаем матрицу из файла
    matrix2 = load_from_mtx("matrix.mtx")
    if matrix2:
        matrix2.print_matrix()


if __name__ == "__main__":
    main()
