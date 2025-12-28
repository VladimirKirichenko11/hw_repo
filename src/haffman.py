import heapq
import os
import pickle
from collections import Counter
from typing import Tuple, Dict


# Узел дерева
class Node:
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# Построение дерева
def build_huffman_tree(text: str) -> Node:
    if not text:
        return None
    # Подсчет частот символов
    frequency = Counter(text)
    # Создание приоритетной очереди
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0] if heap else None


# Построение таблицы кодов
def build_codes_table(
    root: Node, code: str = "", table: Dict[str, str] = None
) -> Dict[str, str]:
    if table is None:
        table = {}
    if root is None:
        return table
    if root.char is not None:
        table[root.char] = code if code else "0"
    else:
        build_codes_table(root.left, code + "0", table)
        build_codes_table(root.right, code + "1", table)

    return table


# Кодирование текста с помощью алгоритма Хаффмана
def encode(msg: str) -> Tuple[str, Dict[str, str]]:
    if not msg:
        return "", {}
    root = build_huffman_tree(msg)
    codes_table = build_codes_table(root)
    # Кодирование сообщения
    encoded_bits = "".join(codes_table[char] for char in msg)
    return encoded_bits, codes_table


# Декодирование текста с помощью таблицы кодов Хаффмана
def decode(encoded: str, table: Dict[str, str]) -> str:
    if not encoded:
        return ""
    # Если в таблице всего один символ
    if len(table) == 1:
        char = next(iter(table))
        return char * len(encoded)
    # Создание обратной таблицы (код -> символ)
    reverse_table = {code: char for char, code in table.items()}
    # Декодирование
    decoded_chars = []
    current_code = ""
    for bit in encoded:
        current_code += bit
        if current_code in reverse_table:
            decoded_chars.append(reverse_table[current_code])
            current_code = ""
    return "".join(decoded_chars)


# Дополнение битовой строки
def pad_encoded_bits(encoded_bits: str) -> Tuple[str, int]:
    padding = 8 - (len(encoded_bits) % 8)
    if padding == 8:
        padding = 0
    padded_bits = encoded_bits + "0" * padding
    return padded_bits, padding


# Преобразование строки битов в байты
def bits_to_bytes(bits: str) -> bytes:
    if len(bits) % 8 != 0:
        raise ValueError("Длина битовой строки должна быть кратна 8")
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i : i + 8]
        byte_array.append(int(byte, 2))
    return bytes(byte_array)


# Преобразование байтов в строку битов
def bytes_to_bits(byte_data: bytes) -> str:
    bits = "".join(format(byte, "08b") for byte in byte_data)
    return bits


# Кодирование файла с использованием алгоритма Хаффмана
def encode_file(input_file: str, output_file: str):
    # Чтение исходного файла
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except UnicodeDecodeError:
        # Если не получилось как текст, читаем как бинарный
        with open(input_file, "rb") as f:
            text = f.read().decode("latin-1")
    # Кодирование текста
    encoded_bits, codes_table = encode(text)
    # Дополнение до целого числа байтов
    padded_bits, padding = pad_encoded_bits(encoded_bits)
    # Преобразование в байты
    encoded_bytes = bits_to_bytes(padded_bits)
    # Формирование заголовка с метаданными
    header = {
        "codes_table": codes_table,
        "padding": padding,
        "original_length": len(text),
    }
    # Сериализация заголовка и данных
    with open(output_file, "wb") as f:
        # Сначала записываем размер заголовка (4 байта)
        header_bytes = pickle.dumps(header)
        header_size = len(header_bytes)
        f.write(header_size.to_bytes(4, "big"))
        # Затем сам заголовок
        f.write(header_bytes)

        # И закодированные данные
        f.write(encoded_bytes)


# Декодирование файла, закодированного алгоритмом Хаффмана
def decode_file(input_file: str, output_file: str):
    with open(input_file, "rb") as f:
        # Чтение размера заголовка
        header_size_bytes = f.read(4)
        if len(header_size_bytes) < 4:
            raise ValueError("Некорректный формат файла")
        header_size = int.from_bytes(header_size_bytes, "big")
        # Чтение заголовка
        header_bytes = f.read(header_size)
        header = pickle.loads(header_bytes)
        # Чтение закодированных данных
        encoded_bytes = f.read()
    # Извлечение метаданных
    codes_table = header["codes_table"]
    padding = header["padding"]
    # Преобразование байтов в биты
    encoded_bits = bytes_to_bits(encoded_bytes)
    # Удаление дополнения
    if padding > 0:
        encoded_bits = encoded_bits[:-padding]
    # Декодирование
    decoded_text = decode(encoded_bits, codes_table)
    # Запись результата
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(decoded_text)
    except UnicodeEncodeError:
        # Если текст содержит не-UTF8 символы, записываем как бинарный
        with open(output_file, "wb") as f:
            f.write(decoded_text.encode("latin-1"))


# Расчёт степени сжатия
def calculate_compression_ratio(original_file: str, compressed_file: str) -> float:
    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)
    if original_size == 0:
        return 0.0
    return (1 - compressed_size / original_size) * 100


def example_usage():
    print("Пример 1: Кодирование и декодирование текста")
    text = "billyboba"
    print(f"Исходный текст: {text}")
    encoded_bits, codes_table = encode(text)
    print(f"Закодированный текст (биты): {encoded_bits}")
    print(f"Таблица кодов: {codes_table}")
    decoded_text = decode(encoded_bits, codes_table)
    print(f"Декодированный текст: {decoded_text}")
    print(f"Совпадение: {text == decoded_text}")

    print("Пример 2: Работа с файлами")
    # Создаем тестовый файл
    test_text = """Это пример текста для тестирования алгоритма Хаффмана."""
    with open("test_input.txt", "w", encoding="utf-8") as f:
        f.write(test_text)
    # Кодируем файл
    encode_file("test_input.txt", "test_encoded.huff")
    # Декодируем файл
    decode_file("test_encoded.huff", "test_output.txt")
    # Проверяем совпадение
    with open("test_input.txt", "r", encoding="utf-8") as f:
        original = f.read()
    with open("test_output.txt", "r", encoding="utf-8") as f:
        restored = f.read()
    print(f"Файлы совпадают: {original == restored}")
    # Расчет сжатия
    ratio = calculate_compression_ratio("test_input.txt", "test_encoded.huff")
    print(f"Степень сжатия: {ratio:.2f}%")
    # Очистка временных файлов
    for file in ["test_input.txt", "test_encoded.huff", "test_output.txt"]:
        if os.path.exists(file):
            os.remove(file)

    # Пример 3: Специальные случаи
    print("Пример 3: Специальные случаи")
    # Пустая строка
    print("Тест пустой строки:")
    encoded, table = encode("")
    print(f"Закодировано: '{encoded}', Таблица: {table}")
    decoded = decode(encoded, table)
    print(f"Декодировано: '{decoded}'")

    # Один символ
    print("\nТест одного символа:")
    encoded, table = encode("aaaaa")
    print(f"Закодировано: '{encoded}', Таблица: {table}")
    decoded = decode(encoded, table)
    print(f"Декодировано: '{decoded}'")


if __name__ == "__main__":
    example_usage()
