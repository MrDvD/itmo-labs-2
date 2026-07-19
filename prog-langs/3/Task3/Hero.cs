public interface IAttackable
{
  public int TakeDamage(int damage);
}

public interface IArtifact
{
  public void Use(Hero self, Hero target);
}

public abstract class Hero : IAttackable
{
  private IArtifact? artifact;
  public string Name { get; set; }
  public int HP { get; set; }
  public int MAX_HP { get; }
  public int Defense { get; set; }
  public int Attack { get; set; }

  public Hero(string name, int attack, int hp, int defense) :
    this(name, attack, hp, defense, null) {}

  public Hero(string name, int attack, int hp, int defense, IArtifact? artifact)
  {
    Name = name;
    Attack = attack;
    HP = hp;
    MAX_HP = hp;
    Defense = defense;
    if (artifact != null)
    {
      this.artifact = artifact;
    }
  }

  public int TakeDamage(int damage)
  {
    if (damage < 0 || damage < Defense)
      return 0;
    int delta = damage - Defense;
    HP -= delta;
    return delta;
  }

  public bool HasArtifact()
  {
    return artifact != null;
  }
    
  public IArtifact GetArtifact()
  {
    if (!HasArtifact())
    {
      throw new Exception("Герой не имеет артефакта.");
    }
    return artifact;
  }

  public abstract void SpecialAbility(Hero target);

  public override string ToString()
  {
    return $"[Name = {Name}, HP = {HP}, Attack = {Attack}, Defense = {Defense}]";
  }
}