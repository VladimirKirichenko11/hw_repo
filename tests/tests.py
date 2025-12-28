import random
import unittest

from sorting import bubble_sort, heap_sort, selection_sort


class Test(unittest.TestCase):
    # Крайние случаи

    def test_empty_array(self):
        input_array = []
        result = heap_sort(input_array)
        self.assertEqual(result, [])

    def test_one_element(self):
        input_array = [1]
        result = heap_sort(input_array)
        self.assertEqual(result, [1])

    def test_all_the_same(self):
        input_array = [1, 1, 1, 1]
        result = heap_sort(input_array)
        self.assertEqual(result, [1, 1, 1, 1])

    # Обычные unit тесты

    def test_two_elements(self):
        input_array = [5, 3]
        result = heap_sort(input_array)
        self.assertEqual(result, [3, 5])

    def test_already_sorted(self):
        input_array = [1, 2, 3, 4, 5]
        result = heap_sort(input_array)
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_reversed_sorted(self):
        input_array = [5, 4, 3, 2, 1]
        result = heap_sort(input_array)
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_with_repetitions(self):
        input_array = [3, 2, 4, 4, 1]
        result = heap_sort(input_array)
        self.assertEqual(result, [1, 2, 3, 4, 4])

    def test_with_negative_numbers(self):
        input_array = [-2, 1, -1, 3, 4]
        result = heap_sort(input_array)
        self.assertEqual(result, [-2, -1, 1, 3, 4])

    def test_with_float_numbers(self):
        input_array = [1.2, 0.37, 2.18, 1.89]
        result = heap_sort(input_array)
        self.assertEqual(result, [0.37, 1.2, 1.89, 2.18])

    # Property based тесты с другими сортировками

    def test_all_sorts_gives_same_result(self):
        test_cases = []
        for _ in range(10):
            size = random.randint(0, 50)
            test_cases.append([random.randint(-100, 100) for _ in range(size)])
        for test_arr in test_cases:
            with self.subTest(input_array=test_arr):
                heap_result = heap_sort(test_arr)
                bubble_result = bubble_sort(test_arr)
                selection_result = selection_sort(test_arr)
                self.assertEqual(heap_result, bubble_result)
                self.assertEqual(heap_result, selection_result)

    def test_sorting_preserves_elements(self):
        for _ in range(10):
            size = random.randint(0, 50)
            original = [random.randint(-100, 100) for _ in range(size)]
            heap_sorted = heap_sort(original)
            bubble_sorted = bubble_sort(original)
            selection_sorted = selection_sort(original)
            self.assertEqual(sorted(original), heap_sorted)
            self.assertEqual(sorted(original), bubble_sorted)
            self.assertEqual(sorted(original), selection_sorted)

    def test_result_is_actually_sorted(self):
        for _ in range(10):
            size = random.randint(0, 50)
            test_arr = [random.randint(-100, 100) for _ in range(size)]
            for sort_func in [heap_sort, bubble_sort, selection_sort]:
                with self.subTest(sort_function=sort_func.__name__):
                    result = sort_func(test_arr)
                    for i in range(len(result) - 1):
                        self.assertLessEqual(result[i], result[i + 1])


if __name__ == "__main__":
    unittest.main()
