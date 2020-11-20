using RatventureCore.Enums;

namespace RatventureCore.Api
{
    public interface IAttackOutcome
    {
        AttackResult Result { get; }

        bool EnemyImmuned { get; }

        int DamageToHero { get; }

        int DamageToEnemy { get; }
    }
}
