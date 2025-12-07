# Функция, возвращающая НОД и коэффициенты Безу
def nod(digit_1, digit_2):
    original_digit_1, original_digit_2 = (
        digit_1,
        digit_2,
    )  # Сохраняем значения чисел, НОД которых будем искать
    x0, x1 = 1, 0  # Коэффициенты digit1, т. к. digit1 = digit1 * 1 + digit2 * 0
    y0, y1 = 0, 1  # Аналогично c digit2
    while digit_2 != 0:
        quotient = digit_1 // digit_2
        digit_1, digit_2 = digit_2, digit_1 % digit_2
        # Обновляем коэффициенты
        x0, x1 = x1, x0 - quotient * x1
        y0, y1 = y1, y0 - quotient * y1
    if original_digit_1 < 0:
        x0 = -x0
    if original_digit_2 < 0:
        y0 = -y0
    return abs(digit_1), x0, y0


digit1 = int(input("Введите первое число "))
digit2 = int(input("Введите второе число "))
gcd, x, y = nod(digit1, digit2)
print("Наибольший общий делитель равен", gcd)
print(f"Соотношение Безу: {digit1}*({x}) + {digit2}*({y}) = {gcd}")
