def heapify(arr, size, i):  # i - индекс корневого элемента
    largest = i  # Инициализируем наибольший элемент как корневой элемент
    left = 2 * i + 1  # Левый потомок
    right = 2 * i + 2  # Правый потомок
    if left < size and arr[i] < arr[left]:
        largest = left
    if right < size and arr[largest] < arr[right]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        # Рекурсивно применяем heapify к затронутому поддереву
        heapify(arr, size, largest)


# Основная функция для сортировки кучей
def heap_sort(arr):
    arr_copy = arr.copy()  # Создаём копию, чтобы не изменять оригинальный массив
    n = len(arr_copy)
    # Проходим по всем элементам снизу вверх
    for i in range(
        n // 2 - 1, -1, -1
    ):  # Обрабатываем только элементы, у которых есть потомки
        heapify(arr_copy, n, i)
    # Один за другим извлекаем элементы
    for i in range(n - 1, 0, -1):
        arr_copy[i], arr_copy[0] = arr_copy[0], arr_copy[i]
        heapify(arr_copy, i, 0)
    return arr_copy


# Функция сортировки пузырьком
def bubble_sort(arr):
    arr_copy = arr.copy()
    n = len(arr_copy)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        if not swapped:
            break
    return arr_copy


def selection_sort(arr):
    arr_copy = arr.copy()
    n = len(arr_copy)
    for i in range(n):
        # Предполагаем, что минимальный элемент на текущей позиции
        min_index = i
        # Ищем минимальный элемент в оставшейся части
        for j in range(i + 1, n):
            if arr_copy[j] < arr_copy[min_index]:
                min_index = j
        arr_copy[i], arr_copy[min_index] = arr_copy[min_index], arr_copy[i]
    return arr_copy
