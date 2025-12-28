from functools import wraps
from inspect import signature
from typing import Callable


def curry(func: Callable, arity: int = None) -> Callable:
    # Проверяем, что func - вызываемый объект
    if not callable(func):
        raise TypeError(f"Ожидался вызываемый объект, получен {type(func)}")

    # Если арность не указана, пытаемся определить её автоматически
    if arity is None:
        try:
            # Получаем количество позиционных параметров
            sig = signature(func)
            arity = sum(
                1
                for param in sig.parameters.values()
                if param.default == param.empty
                and param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD)
            )
        except (ValueError, TypeError):
            raise ValueError("Не удалось определить арность функции. Укажите её явно.")

    # Проверяем корректность арности
    if arity < 0:
        raise ValueError(f"Арность не может быть отрицательной: {arity}")

    # Кэшируем арность для использования в рекурсивной функции
    @wraps(func)
    def curried(*args):
        if len(args) == arity:
            # Все аргументы получены - вызываем оригинальную функцию
            return func(*args)
        elif len(args) > arity:
            # Получено больше аргументов, чем ожидалось
            raise TypeError(f"Функция ожидает {arity} аргументов, получено {len(args)}")
        else:
            # Частичное применение - возвращаем новую каррированную функцию
            def partial(*next_args):
                return curried(*(args + next_args))

            # Обновляем количество оставшихся аргументов
            partial.__name__ = f"{func.__name__}_curried_{len(args)}_of_{arity}"
            return partial

    # Сохраняем оригинальную функцию и арность для возможного использования
    curried._original_func = func
    curried._arity = arity
    curried.__name__ = f"curried_{func.__name__}"

    return curried


def uncurry(curried_func: Callable, arity: int = None) -> Callable:
    # Проверяем, что curried_func - вызываемый объект
    if not callable(curried_func):
        raise TypeError(f"Ожидался вызываемый объект, получен {type(curried_func)}")

    # Если арность не указана, пытаемся определить её из атрибутов функции
    if arity is None:
        if hasattr(curried_func, "_arity"):
            arity = curried_func._arity
        else:
            # Пытаемся определить арность эмпирически
            # (для чисто каррированных функций без побочных эффектов)
            raise ValueError("Не удалось определить арность. Укажите её явно.")

    # Проверяем корректность арности
    if arity < 0:
        raise ValueError(f"Арность не может быть отрицательной: {arity}")

    @wraps(curried_func)
    def uncurried(*args):
        # Проверяем количество аргументов
        if len(args) != arity:
            raise TypeError(f"Функция ожидает {arity} аргументов, получено {len(args)}")

        # Последовательно применяем аргументы к каррированной функции
        result = curried_func
        for arg in args:
            result = result(arg)
        return result

    # Сохраняем оригинальную функцию и арность
    uncurried._original_func = curried_func
    uncurried._arity = arity
    uncurried.__name__ = f"uncurried_{curried_func.__name__}"
    return uncurried


# Пример использования из задания
def sum3(x, y, z):
    return x + y + z


# Тестирование
if __name__ == "__main__":
    print("\nПример 1: Базовый пример из задания")
    sum3_curry = curry(sum3, 3)
    sum3_uncurry = uncurry(sum3_curry, 3)
    print(f"sum3_curry(1)(2)(3) = {sum3_curry(1)(2)(3)}")  # 6
    print(f"sum3_uncurry(1, 2, 3) = {sum3_uncurry(1, 2, 3)}")  # 6

    print("\nПример 2: Частичное применение")
    add5 = sum3_curry(2)(3)  # Частично применяем первые два аргумента
    print(f"add5(10) = {add5(10)}")  # 2 + 3 + 10 = 15

    print("\nПример 3: Функция с двумя аргументами")

    def multiply(x, y):
        return x * y

    multiply_curry = curry(multiply, 2)
    double = multiply_curry(2)
    print(f"double(5) = {double(5)}")  # 10
    print(f"multiply_curry(3)(4) = {multiply_curry(3)(4)}")  # 12

    print("\nПример 4: Проверка ошибок")
    try:
        # Неверная арность (отрицательная)
        bad_curry = curry(sum3, -1)
    except ValueError as e:
        print(f"Ошибка при отрицательной арности: {e}")

    try:
        # Слишком много аргументов при вызове
        sum3_curry(1, 2, 3, 4)
    except TypeError as e:
        print(f"Ошибка при слишком большом количестве аргументов: {e}")

    try:
        # Слишком много аргументов при uncurry
        sum3_uncurry(1, 2, 3, 4)
    except TypeError as e:
        print(f"Ошибка uncurry при слишком большом количестве аргументов: {e}")

    try:
        # Слишком мало аргументов при uncurry
        sum3_uncurry(1, 2)
    except TypeError as e:
        print(f"Ошибка uncurry при слишком малом количестве аргументов: {e}")
