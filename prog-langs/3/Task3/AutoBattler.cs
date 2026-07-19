class Team
{
  List<Hero> alive = new List<Hero>();
  Random random = new Random();
  public bool IsAlive()
  {
    return alive.Count > 0;
  }
  public Hero GetHero()
  {
    if (!IsAlive())
    {
      throw new Exception("Нет живых героев.");
    }
    return alive[random.Next(0, alive.Count)];
  }
  public bool ValidateHero(Hero hero)
  {
    bool isDead = hero.HP <= 0;
    if (isDead)
    {
      RemoveHero(hero);
    }
    return !isDead;
  }
  public void RemoveHero(Hero hero)
  {
    alive.Remove(hero);
  }
  public Team(List<Hero> heroes)
  {
    foreach (Hero hero in heroes)
    {
      if (hero.HP > 0)
      {
        alive.Add(hero);
      }
    }
  }
}

class AutoBattler(Team team1, Team team2, string logfile)
{
  Random random = new Random();
  public void Duel(Hero hero1, Hero hero2, int step)
  {
    ConsoleUtils.Log($"{hero1.Name} ({hero1.HP} HP) vs {hero2.Name} ({hero2.HP} HP)", ConsoleColor.Gray, logfile);
    if (step % 5 == 0)
    {
      if (hero1.HasArtifact() && hero2.HasArtifact())
      {
        if (random.Next(0, 2) == 0)
        {
          hero1.GetArtifact().Use(hero1, hero2);
          ConsoleUtils.Log($"{hero1.Name} применил артефакт!", ConsoleColor.DarkCyan, logfile);
        }
        else
        {
          hero2.GetArtifact().Use(hero2, hero1);
          ConsoleUtils.Log($"{hero2.Name} применил артефакт!", ConsoleColor.DarkCyan, logfile);
        }
      } else if (hero1.HasArtifact())
      {
        hero1.GetArtifact().Use(hero1, hero2);
        ConsoleUtils.Log($"{hero1.Name} применил артефакт!", ConsoleColor.DarkCyan, logfile);
      } else if (hero2.HasArtifact())
      {
        hero2.GetArtifact().Use(hero2, hero1);
        ConsoleUtils.Log($"{hero2.Name} применил артефакт!", ConsoleColor.DarkCyan, logfile);
      } else
      {
        ConsoleUtils.Log("Никто не применил артефакт.", ConsoleColor.DarkCyan, logfile);
      }
    }
    if (step % 3 == 0)
    {
      if (random.Next(0, 2) == 0)
      {
        hero1.SpecialAbility(hero2);
        ConsoleUtils.Log($"{hero1.Name} применил суперспособность!", ConsoleColor.DarkCyan, logfile);
      }
      else
      {
        hero2.SpecialAbility(hero1);
        ConsoleUtils.Log($"{hero2.Name} применил свою суперспособность!", ConsoleColor.DarkCyan, logfile);
      }
      return;
    }
    int damage2 = hero2.TakeDamage(hero1.Attack);
    ConsoleUtils.Log($"{hero2.Name} получил {damage2} урона.", ConsoleColor.DarkYellow, logfile);
    int damage1 = hero1.TakeDamage(hero2.Attack);
    ConsoleUtils.Log($"{hero1.Name} получил {damage1} урона.", ConsoleColor.DarkYellow, logfile);
  }
  public void Run()
  {
    ConsoleUtils.ClearFile(logfile);
    ConsoleUtils.Log("Начало автоматической битвы.", ConsoleColor.Black, logfile);
    int step = 0;
    while (team1.IsAlive() && team2.IsAlive())
    {
      step++;
      Hero hero1 = team1.GetHero();
      Hero hero2 = team2.GetHero();
      ConsoleUtils.Log($"Ход #{step}.", ConsoleColor.Gray, logfile);
      Duel(hero1, hero2, step);
      if (!team1.ValidateHero(hero1))
      {
        ConsoleUtils.Log($"{hero1.Name} выбыл из первой команды.", ConsoleColor.Red, logfile);
      }
      if (!team2.ValidateHero(hero2))
      {
        ConsoleUtils.Log($"{hero2.Name} выбыл из второй команды.", ConsoleColor.Red, logfile);
      }
    }
    if (team1.IsAlive())
    {
      ConsoleUtils.Log("Первая команда победила!", ConsoleColor.Green, logfile);
    }
    else if (team2.IsAlive())
    {
      ConsoleUtils.Log("Вторая команда победила!", ConsoleColor.Green, logfile);
    }
    else
    {
      ConsoleUtils.Log("Никто не одержал победу!", ConsoleColor.Yellow, logfile);
    }
    ConsoleBeeps.success();
  }
}