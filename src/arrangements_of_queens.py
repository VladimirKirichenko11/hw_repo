import itertools

# Переборное решение
def queens_brute_force(n):
    count = 0
    # Генерируем все перестановки чисел от 0 до n-1
    # Каждая перестановка представляет расстановку ферзей:
    # индекс - строка, значение - столбец
    for permutation in itertools.permutations(range(n)):
        if is_valid(permutation):
            count += 1
    return count

# Проверяем не бьют ли ферзи друг друга по диагонали
def is_valid(board):
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            # Проверка на одну диагональ:
            # разность строк равна разности столбцов
            if abs(i - j) == abs(board[i] - board[j]):
                return False
    return True


def queens_backtracking(n):

    def backtrack(row, columns, diagonals1, diagonals2):
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            d1 = row - col  # диагональ \
            d2 = row + col  # диагональ /
            # Проверяем, не находится ли клетка под атакой
            if columns[col] or diagonals1[d1] or diagonals2[d2]:
                continue
            # Ставим ферзя
            columns[col] = True
            diagonals1[d1] = True
            diagonals2[d2] = True
            # Переходим к следующей строке
            backtrack(row + 1, columns, diagonals1, diagonals2)
            # Убираем ферзя
            columns[col] = False
            diagonals1[d1] = False
            diagonals2[d2] = False
    count = 0
    # Используем массивы для быстрой проверки
    columns = [False] * n
    diagonals1 = [False] * (2 * n - 1)  # диагонали \
    diagonals2 = [False] * (2 * n - 1)  # диагонали /
    backtrack(0, columns, diagonals1, diagonals2)
    return count

# Самое быстрое решение
def queens_bitwise(n):

    def solve(row, columns, diagonals1, diagonals2, count):
        # Если все строки заполнены
        if row == n:
            return count + 1
        # Определяем, какие клетки доступны в текущей строке
        available = (~(columns | diagonals1 | diagonals2)) & ((1 << n) - 1)
        while available:
            # Берем самую правую доступную позицию
            position = available & -available
            available -= position
            # Рекурсивно обрабатываем следующую строку
            count = solve(
                row + 1,
                columns | position,
                (diagonals1 | position) << 1,
                (diagonals2 | position) >> 1,
                count
            )
        return count
    # Используем битовые маски:
    # columns - занятые столбцы
    # diagonals1 - занятые диагонали \
    # diagonals2 - занятые диагонали /
    return solve(0, 0, 0, 0, 0)

def main():
    # Тестирование всех трех версий
    n = int(input("Введите N: "))
    print("1. Переборное решение:")
    if n <= 10:  # Переборное решение медленное для больших N
        result1 = queens_brute_force(n)
        print(f"   Количество расстановок: {result1}")
    else:
        print("   Слишком большое N для перебора")
    print("2. Рекурсивное решение с возвратом:")
    result2 = queens_backtracking(n)
    print(f"   Количество расстановок: {result2}")
    print("3. Оптимизированное решение:")
    result3 = queens_bitwise(n)
    print(f"   Количество расстановок: {result3}")

if __name__ == "__main__":
    main()