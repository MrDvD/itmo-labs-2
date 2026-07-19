public static class ConsoleUtils
{
  public static void Log(string data, ConsoleColor color)
  {
    Console.ForegroundColor = color;
    Console.WriteLine(data);
    Console.ResetColor();
  }

  public static void ClearFile(string file)
  {
    File.WriteAllText(Path.Combine(Environment.CurrentDirectory, file), "");
  }

  public static void Log(string data, ConsoleColor color, string file)
  {
    Log(data, color);
    File.AppendAllText(Path.Combine(Environment.CurrentDirectory, file), data + "\n");
  }
}

public static class ConsoleBeeps
{
  public static void success()
  {
    Console.WriteLine("\a");
    Console.Beep();
  }
}