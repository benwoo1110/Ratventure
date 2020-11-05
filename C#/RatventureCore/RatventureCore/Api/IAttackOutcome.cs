using RatventureCore.Enums;

namespace RatventureCore.Api
{
    public interface IAttackOutcome
    {
        bool IsResult(AttackResult result);

        AttackResult Result { get; set; }

        bool EnemyImmuned { get; set; }

        int DamageToHero { get; set; }

        int DamageToEnemy { get; set; }
    }
}
