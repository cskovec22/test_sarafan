from typing import Iterator


def sequence_gen() -> Iterator[int]:
    """
    Создать бесконечную последовательность чисел.

    Каждое число в последовательности повторяется столько раз, чему оно равно.
    Например, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4... и так далее.

        Возвращаемые значения:
            num (Iterator[int]): целое число бесконечной последовательности.
    """
    num: int = 1

    while True:
        for _ in range(num):
            yield num
        num += 1


def get_sequence(sequence_gen: Iterator[int], count_elements: int) -> str:
    """Получить последовательность чисел в виде строки.

        Параметры:
            sequence_gen (Iterator[int]): целое число бесконечной
                последовательности;
            count_elements (int): количество элементов последовательности.

        Возвращаемые значения:
            (str): строка последовательности чисел длиной count_elements.
    """
    sequence_list: list[str] = [
        str(next(sequence_gen)) for _ in range(count_elements)
    ]
    return "".join(sequence_list)


count_elements = input(
    "Введите количество элементов последовательности "
    "(целое положительное число): "
)
if not count_elements.isdigit():
    raise ValueError("Ошибка ввода числа!")

sequence: Iterator[int] = sequence_gen()
print(get_sequence(sequence, int(count_elements)))
