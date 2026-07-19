// https://raw.githubusercontent.com/sahildit/IMDB-Movies-Extensive-Dataset-Analysis/refs/heads/master/data1/IMDb%20movies.csv
using Microsoft.VisualBasic.FileIO;

List<string[]> ReadAllCsvLines(string filePath)
{
    var result = new List<string[]>();

    using (var parser = new TextFieldParser(filePath))
    {
        parser.TextFieldType = FieldType.Delimited;
        parser.SetDelimiters(",");
        parser.HasFieldsEnclosedInQuotes = true;

        while (!parser.EndOfData)
        {
            string[] fields = parser.ReadFields();
            result.Add(fields);
        }
    }

    return result;
}

var result = ReadAllCsvLines("movies.csv");

// #1
Console.WriteLine("### 1. Преобразовать в класс Movie");
var movies = result.Skip(1)
                   .Select(movie => new Movie(movie[1],
                                              int.TryParse(movie[3], out int result) ? result : 0,
                                              movie[5],
                                              movie[9],
                                              float.TryParse(movie[20], out float floatRes) ? floatRes : 0))
                   .ToList();
movies.Take(5).ToList().ForEach(Console.WriteLine);

// #2
var desiredDirector = "Christopher Nolan";
Console.WriteLine("### 2. Найти все фильмы режиссёра {0}", desiredDirector);
var directorInvariant = desiredDirector;
var directorFilter = movies.Where(movie => movie.director.Contains(directorInvariant, StringComparison.InvariantCultureIgnoreCase)).ToList();
directorFilter.ForEach(Console.WriteLine); 

// #3
Console.WriteLine("### 3. Пять самый высокооценённых фильма, выпущенных после 2010");
var most = movies.Where(x => x.year > 2010)
                 .OrderByDescending(x => x.metascore)
                 .Take(5)
                 .ToList();
var idx = 0;
most.ForEach(x => {
  Console.WriteLine("{0}. {1}", ++idx, x);
});

// #4
var desiredGenreName = "Drama";
var invariantGenre = desiredGenreName;
// g1, g2
// g1,g2
Console.WriteLine("### 4. Получить список фильмов (их количество и средний рейтинг) жанра {0}", desiredGenreName);
var genre = movies.Where(x => x.genre.Split(",", StringSplitOptions.TrimEntries | StringSplitOptions.RemoveEmptyEntries)
                                     .Where(x => x.Equals(invariantGenre, StringComparison.CurrentCultureIgnoreCase))
                                     .Any())
                  .ToList();
Console.WriteLine("количество: {0}, средний рейтинг: {1}", genre.Count, genre.Average(x => x.metascore));

// #5
Console.WriteLine("### 5. Режиссёр, у которого больше всего фильмов");
var directorMost = movies.Where(x => !string.IsNullOrWhiteSpace(x.director))
                         .SelectMany(x => x.director.Split(",", StringSplitOptions.TrimEntries | StringSplitOptions.RemoveEmptyEntries),
                                     (movie, director) => new { Movie = movie, Director = director })
                         .GroupBy(x => x.Director)
                         .OrderByDescending(group => group.Count())
                         .First()
                         .ToList();
Console.WriteLine("режиссёр: {0}, количество: {1}", directorMost.First().Director, directorMost.Count);
Console.WriteLine("пять его фильмов:");
directorMost.Take(5).ToList().ForEach(Console.WriteLine);

// var splistr = "A, B, C".Split(',');
// var intTest = int.TryParse("122", out var intResult) ? intResult : 0;

// 1. Преобразовать в класс Movie (нужно создать класс) - Select
// Над списком из Movie 
// 2. Найти все фильмы режисёра/актёра/продюсера (на выбор, например Nolan) - Where
// 3. 5 самый высокооценённых фильма выпущенных после 2010 
// 4. Получить список фильмов (их количество и средний рейтинг) любого жанра (на выбор, например Drama) 
// 5. Режисёр у которого больше всего фильмов
// Не учитывать регистр
// Обработать поля с несколькими значениями