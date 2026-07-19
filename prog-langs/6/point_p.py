import ctypes
import os
import time

# TODO
# 1. Создать на питоне скрипт, который генерирует файл, содержащий 1000+ пар чисел
# Пример
# 0,1 1,20 —> расстояние между ними
# 1,20 1,20 
# 3,10 3,10
# 1,0 1,0
# 2. Читаем файл и записываем в массив(ы)
# 3. Массив(ы) содержит класс Point
# 4. Передаём массив(ы) в фунцию написанную на C
# 5. Функция на C для каждой пары считаем расстояние и возвращаем массив с результатами
# 6. Результаты выводим из кода питона
# gcc -shared .\point_lib.c -o point_lib.dll — Windows
# gcc -fPIC -shared .\point_lib.c -o point_lib.so — Linux & MacOS


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)] 

if __name__ == "__main__":
    print("Start program")

    # --- Загрузка библиотеки ---
    # Определение имени файла библиотеки в зависимости от ОС
    lib_name = "point_lib.dll" if os.name == 'nt' else "point_lib.so"
    lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), lib_name)

    try:
        # Загрузка C-библиотеки
        c_lib = ctypes.CDLL(lib_path)
        print(f"Библиотека успешно загружена: {lib_path}")
    except Exception as e:
        print(f"ОШИБКА: Не удалось загрузить библиотеку '{lib_path}'")
        print(f"Детали ошибки: {e}")
        exit()


    c_lib.process_point.argtypes = [ctypes.POINTER(Point)]
    c_lib.process_point.restype = None # (void)

    my_point = Point(x = 5, y = 11)
    print(my_point.x, my_point.y)
    c_lib.process_point(my_point) 
    print("My point:", my_point.x, my_point.y)

    data = []
    ArrayType = ctypes.c_longlong * len(data)   # 1. Создаём тип "массив из N long long"
    c_array = ArrayType(*data)                  # 2. Создаём экземпляр этого массива
    # c_func(c_array)





