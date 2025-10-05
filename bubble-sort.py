from random import randint


# Задаём функцию пузырьковой сортировки
def bubble(array):
    # Проходимся по массиву
    # i - номер текущей итерации
    for i in range(len(array) - 1):
        # Проходимся по ещё не отсортированной части массива
        for j in range((len(array) - 1) - i):
            # Cравниваем элементы массива
            if array[j] > array[j + 1]:  # Если текущий элемент больше следующего
                array[j], array[j + 1] = array[j + 1], array[j]  # То меняем их местами


last = int(input("Введите наибольшее число массива "))
quantity = int(input("Введите количество элементов массива "))
mass = [randint(1, last) for n in range(quantity)]
print(mass)  # Вывод неотсортированного массива
bubble(mass)
print(mass)  # Вывод отсортированного массива
