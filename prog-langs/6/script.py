import ctypes, random, os

class Point(ctypes.Structure):
  _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]

  def __str__(self):
    return f"({self.x}, {self.y})"

PAIR_COUNT = 5
TuplePoint = Point * 2
ArrayPoint = ctypes.POINTER(TuplePoint) * PAIR_COUNT
ResultList = ctypes.c_double * PAIR_COUNT

def create_file(filename, pair_count = PAIR_COUNT):
  with open(filename, "w") as f:
    for _ in range(pair_count):
      coords = list()
      for _ in range(4):
        coords.append(str(random.randint(-100, 100)))
      f.write(",".join(coords[:2]) + " " + ",".join(coords[2:]) + "\n")

def read_file_to_arr(filename):
  with open(filename) as f:
    arr = list()
    for line in f.readlines():
      pt1, pt2 = line.split()
      x1, y1 = pt1.split(",")
      x2, y2 = pt2.split(",")
      p1, p2 = Point(x = int(x1), y = int(y1)), Point(x = int(x2), y = int(y2))
      array_pt_line = TuplePoint(p1, p2)
      arr.append(ctypes.pointer(array_pt_line))
  return ArrayPoint(*arr)

def init_c_interop(lib_name="point_lib.so"):
  lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), lib_name)
  try:
    c_lib = ctypes.CDLL(lib_path)
  except Exception as e:
    print(f"ОШИБКА: Не удалось загрузить библиотеку '{lib_path}'")
    print(f"Детали ошибки: {e}")
    exit()
  return c_lib

def calculate_via_c(arr, c_lib, result):
  c_lib.process_point_arrays.argtypes = [ArrayPoint, ctypes.c_int, ctypes.POINTER(ResultList)]
  return c_lib.process_point_arrays(arr, PAIR_COUNT, result)

def pretty_print(init_arr, result_arr):
  for i in range(PAIR_COUNT):
    print(f"{i + 1}. {init_arr[i][0][0]} - {init_arr[i][0][1]} => {result_arr[i]:.2f}")

def main():
  filename = "file.out"
  c_lib = init_c_interop()
  create_file(filename)
  arr = read_file_to_arr(filename)
  result = ResultList(*[0 for _ in range(PAIR_COUNT)])
  calculate_via_c(arr, c_lib, result)
  pretty_print(arr, result)

if __name__ == "__main__":
  main()