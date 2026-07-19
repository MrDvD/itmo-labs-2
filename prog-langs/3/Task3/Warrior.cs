public class Warrior : Hero
{
  public Warrior(string name, int attack, int hp, int defense) :
      base(name, attack, hp, defense)
  {

  }

  public Warrior(string name, int attack, int hp, int defense, IArtifact artifact) :
    base(name, attack, hp, defense, artifact)
  {

  }

  public override void SpecialAbility(Hero target)
  {
    target.TakeDamage(Attack * 2);
  }
}

public class ShieldRepair : IArtifact
{
  public void Use(Hero self, Hero target)
  {
    self.Defense += 2;
  }
}