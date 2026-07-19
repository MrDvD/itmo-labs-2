// TODO
// Написать программу, которая принимает названия текстовых файлов (можно брать с консоли, аргументов, хардкодить)
// Создаёт на каждый файл таску, которая читает файл и считает количество слов в файле
// Как только таска заканчивается, то нужно вывести сколько слов в файле
// Замерить время выполнение программы

using System.Diagnostics;
using System.Text.RegularExpressions;

string[] filenames = ["files/1", "files/2", "files/3", "files/4", "files/5"];

var st = new Stopwatch();
st.Start();

List<Task> tasks = [];

foreach (var filename in filenames)
{
  tasks.Add(Decorate(filename));
}

await Task.WhenAll(tasks);

Console.WriteLine(st.Elapsed);
// Console.WriteLine(Environment.CurrentManagedThreadId);

static int countWords(string text)
{
  string[] words = MyRegex().Split(text);
  return words.Count(w => !string.IsNullOrEmpty(w));
}

static async Task Decorate(string filename)
{
  await Task.Delay(1000);
  var text = await File.ReadAllTextAsync(filename);
  var count = countWords(text);
  // Console.WriteLine(Environment.CurrentManagedThreadId);
  Console.WriteLine(filename + ": " + count + " words");
}

partial class Program
{
  [GeneratedRegex(@"[^A-Za-zА-Яа-яЁё0-9]")]
  private static partial Regex MyRegex();
}