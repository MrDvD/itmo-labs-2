class Wizard : Hero
{
  public Wizard(string name, int attack, int hp, int defense) :
        base(name, attack, hp, defense)
  {

  }

  public Wizard(string name, int attack, int hp, int defense, IArtifact artifact) :
        base(name, attack, hp, defense, artifact)
  {

  }
  // heals himself by 20 HP
  public override void SpecialAbility(Hero target)
  {
    HP = Math.Min(HP + 20, MAX_HP);
  }
}