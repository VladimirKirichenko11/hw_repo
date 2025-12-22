# Узел биномиального дерева
class BinomialNode:
    # Инициализация узла биномиального дерева
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.degree = 0  # Степень дерева (количество потомков)
        self.children = []  # Список дочерних узлов
        self.parent = None  # Родительский узел

    # Добавление дочернего узла
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        self.degree += 1


# Очередь с приоритетами на основе списка биномиальных деревьев
class BinomialHeap:
    # Инициализация пустой биномиальной кучи
    def __init__(self):
        self.trees = []  # Список корней биномиальных деревьев
        self.min_node = None  # Указатель на узел с минимальным ключом
        self.count = 0  # Количество элементов в куче

    # Проверка кучи на пустоту
    def is_empty(self):
        return self.min_node is None

    # Вставка нового элемента в кучу
    def insert(self, key, value=None):
        # Создаем новую кучу с одним элементом
        new_heap = BinomialHeap()
        new_node = BinomialNode(key, value)
        new_heap.trees = [new_node]
        new_heap.min_node = new_node
        new_heap.count = 1
        self.merge(new_heap)  # Объединяем с текущей кучей
        return new_node

    # Получение минимального элемента (без удаления)
    def get_min(self):
        if self.min_node:
            return self.min_node.key, self.min_node.value
        return None

    # Извлечение минимального элемента
    def extract_min(self):
        if self.is_empty():
            return None
        min_node = self.min_node
        self.trees.remove(min_node)
        # Создаем новую кучу из потомков минимального узла
        children_heap = BinomialHeap()
        # Меняем порядок потомков для сохранения порядка по возрастанию степени
        for child in reversed(min_node.children):
            child.parent = None
            children_heap.trees.append(child)
        children_heap.count = len(min_node.children)
        children_heap._find_min()  # Находим новый минимум в куче детей
        # Уменьшаем общее количество элементов
        self.count -= 1 + len(min_node.children)
        # Объединяем текущую кучу с кучей потомков
        self.merge(children_heap)
        return min_node.key, min_node.value

    # Объединение двух биномиальных куч
    def merge(self, other_heap):
        # Объединяем списки деревьев
        self.trees.extend(other_heap.trees)
        self.count += other_heap.count
        if self.min_node is None or (
            other_heap.min_node and other_heap.min_node.key < self.min_node.key
        ):
            self.min_node = other_heap.min_node
        # Выполняем объединение деревьев одинаковой степени
        self._consolidate()

    # Объединение деревьев одинаковой степени в куче
    def _consolidate(self):
        if not self.trees:
            self.min_node = None
            return
        # Создаем массив для хранения деревьев по их степени
        degree_to_tree = [None] * (self.count.bit_length() + 1)
        i = 0
        while i < len(self.trees):
            current = self.trees[i]
            current_degree = current.degree
            # Если есть дерево с такой же степенью, объединяем их
            while degree_to_tree[current_degree] is not None:
                same_degree_tree = degree_to_tree[current_degree]
                # Определяем, какое дерево станет корнем (с меньшим ключом)
                if current.key > same_degree_tree.key:
                    current, same_degree_tree = same_degree_tree, current
                # Делаем дерево с большим ключом потомком
                current.add_child(same_degree_tree)
                # Удаляем объединенное дерево из списка
                self.trees.remove(same_degree_tree)
                degree_to_tree[current_degree] = None
                current_degree += 1
            # Сохраняем дерево в массиве по его новой степени
            degree_to_tree[current_degree] = current
            i += 1
        # Находим новый минимальный узел
        self._find_min()

    # Поиск минимального узла среди корней деревьев
    def _find_min(self):
        if not self.trees:
            self.min_node = None
            return
        self.min_node = self.trees[0]
        for tree in self.trees[1:]:
            if tree.key < self.min_node.key:
                self.min_node = tree

    # Уменьшение ключа у узла
    def decrease_key(self, node, new_key):
        if new_key > node.key:
            return False
        node.key = new_key
        parent = node.parent
        # Поднимаем узел вверх, если его ключ меньше родительского
        while parent is not None and node.key < parent.key:
            # Меняем ключи и значения
            node.key, parent.key = parent.key, node.key
            node.value, parent.value = parent.value, node.value
            # Переходим к родителю
            node = parent
            parent = node.parent
        # Обновляем минимум
        if node.key < self.min_node.key:
            self.min_node = node
        return True

    # Количество элементов в куче
    def __len__(self):
        return self.count

    # Строковое представление кучи
    def __repr__(self):
        return f"BinomialHeap(trees={len(self.trees)}, min_key={self.min_node.key if self.min_node else None})"


# Дополнительный класс для удобного интерфейса очереди с приоритетами
class PriorityQueue:

    def __init__(self):
        """Инициализация пустой очереди с приоритетами."""
        self.heap = BinomialHeap()

    # Добавление элемента в очередь
    def enqueue(self, priority, value):
        return self.heap.insert(priority, value)

    # Извлечение элемента с меньшим ключом
    def dequeue(self):
        result = self.heap.extract_min()
        return result[1] if result else None

    # Просмотр элемента с наибольшим приоритетом (без удаления)
    def peek(self):
        result = self.heap.get_min()
        return result[1] if result else None

    # Проверка очереди на пустоту
    def is_empty(self):
        return self.heap.is_empty()

    # Количество элементов в очереди
    def __len__(self):
        return len(self.heap)

    # Извлечение приоритета элемента
    def change_priority(self, node, new_priority):
        return self.heap.decrease_key(node, new_priority)


# Пример использования и тестирование
def main():
    # Создаем очередь с приоритетами
    pq = PriorityQueue()
    # Добавляем элементы
    print("Добавляем элементы в очередь:")
    nodes = []
    nodes.append(pq.enqueue(5, "Task 5"))
    nodes.append(pq.enqueue(1, "Task 1"))
    nodes.append(pq.enqueue(3, "Task 3"))
    nodes.append(pq.enqueue(2, "Task 2"))
    nodes.append(pq.enqueue(4, "Task 4"))

    print(f"Очередь содержит {len(pq)} элементов")
    print(f"Следующий элемент: {pq.peek()}")
    print()

    # Извлекаем элементы в порядке приоритета
    print("Извлекаем элементы в порядке приоритета:")
    while not pq.is_empty():
        task = pq.dequeue()
        print(f"Извлечено: {task}")

    print()

    # Тестирование слияния двух куч
    print("Тестирование слияния двух куч:")
    heap1 = BinomialHeap()
    heap2 = BinomialHeap()
    heap1.insert(10, "A")
    heap1.insert(20, "B")
    heap1.insert(5, "C")
    heap2.insert(15, "D")
    heap2.insert(3, "E")
    heap2.insert(7, "F")
    print(f"Куча 1 минимум: {heap1.get_min()}")
    print(f"Куча 2 минимум: {heap2.get_min()}")
    heap1.merge(heap2)
    print(f"После слияния минимум: {heap1.get_min()}")
    print(f"Всего элементов: {len(heap1)}")
    print()
    # Тестирование уменьшения ключа
    print("Тестирование уменьшения ключа:")
    heap = BinomialHeap()
    heap.insert(10, "Item 10")
    heap.insert(20, "Item 20")
    node3 = heap.insert(30, "Item 30")
    print(f"Минимум до уменьшения: {heap.get_min()}")
    heap.decrease_key(node3, 1)
    print(f"Минимум после уменьшения: {heap.get_min()}")


if __name__ == "__main__":
    main()
