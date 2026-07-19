class Movie(string title, int year, string genre, string director, float metascore)
{
  public readonly string title = title;
  public readonly int year = year;
  public readonly string genre = genre;
  public readonly string director = director;
  public readonly float metascore = metascore;
  public override string ToString()
  {
    return string.Format("Movie{{Название: {0}, Год: {1}, Жанр: {2}, Режиссёр: {3}, Рейтинг: {4}}}", title, year, genre, director, metascore);
  }
}