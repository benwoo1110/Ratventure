using Ratventure.Core.Enums;

namespace Ratventure.Core.Api
{
    public interface IAttackOutcome
    {
        bool IsResult(AttackResult result);

        AttackResult Result { get; }

        bool EnemyImmuned { get; }

        int DamageToHero { get; }

        int DamageToEnemy { get; }
    }
}
