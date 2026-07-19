using System.Runtime.InteropServices;

[DllImport("corelib.so", CallingConvention = CallingConvention.Cdecl)]
static extern void filter([In] Point[] dots, [In] int length, [In] ConditionFunc f, [Out] Point[] result);

String fileName = "dots.txt";

using var reader = new StreamReader(fileName);
string line;
List<Point> list_in = new List<Point>();
while ((line = reader.ReadLine()) != null)
{
  string[] res = line.Split(" ");
  int X = Int32.Parse(res[0]);
  int Y = Int32.Parse(res[1]);
  Point p = new(X, Y);
  list_in.Add(p);
  Console.WriteLine($"Read point from file in C#: ({p.X}, {p.Y})");
}

bool IsFirst(Point p)
{
  return p.X > 0 && p.Y > 0;
}

bool IsSecond(Point p)
{
  return p.X < 0 && p.Y > 0;
}

bool IsThird(Point p)
{
  return p.X < 0 && p.Y < 0;
}

bool IsFourth(Point p)
{
  return p.X > 0 && p.Y < 0;
}

void PrettyPrint(Point[] arr)
{
  foreach (Point p in arr)
  {
    if (p.X != 0 && p.Y != 0)
    {
      Console.WriteLine($"{p.X} {p.Y}");
    }
  }
}

Point[] arr_in = list_in.ToArray();
Point[] arr_1 = new Point[list_in.Count];
Point[] arr_2 = new Point[list_in.Count];
Point[] arr_3 = new Point[list_in.Count];
Point[] arr_4 = new Point[list_in.Count];

Console.WriteLine("--- Starting C filter 1 from C#:");
filter(arr_in, list_in.Count, IsFirst, arr_1);
filter(arr_in, list_in.Count, IsSecond, arr_1);
Console.WriteLine("--- Printing filtered result 1 in C#:");
PrettyPrint(arr_1);
Console.WriteLine("--- Done printing in C#.");
Console.WriteLine("--- Starting C filter 2 from C#:");
filter(arr_in, list_in.Count, IsSecond, arr_2);
Console.WriteLine("--- Printing filtered result 2 in C#:");
PrettyPrint(arr_2);
Console.WriteLine("--- Starting C filter 3 from C#:");
filter(arr_in, list_in.Count, IsThird, arr_3);
Console.WriteLine("--- Printing filtered result 3 in C#:");
PrettyPrint(arr_3);
Console.WriteLine("--- Starting C filter 4 from C#:");
// buf int[65356]
// n, err := read(buf)
filter(arr_in, list_in.Count, IsFourth, arr_4);
Console.WriteLine("--- Printing filtered result 4 in C#:");
PrettyPrint(arr_4);

[StructLayout(LayoutKind.Sequential)]
struct Point(int x, int y)
{
  public int X { get; set; } = x;
  public int Y { get; set; } = y;
}

delegate bool ConditionFunc(Point p);