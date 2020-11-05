using RatventureCore.Api;
using RatventureCore.Enums;

namespace RatventureCore.GamePlay
{
    class AttackOutcome : IAttackOutcome
    {
        private AttackResult result;
        private bool enemyImmuned;
        private int damageToHero;
        private int damageToEnemy;

        public AttackOutcome()
        {
            this.result = AttackResult.Unknown;
            this.enemyImmuned = false;
            this.damageToHero = 0;
            this.damageToEnemy = 0;
        }

        public bool IsResult(AttackResult result)
        {
            return this.result.Equals(result);
        }

        public AttackResult Result
        {
            get => result;
            set => result = value;
        }

        public bool EnemyImmuned
        {
            get => enemyImmuned;
            set => enemyImmuned = value;
        }

        public int DamageToHero
        {
            get => damageToHero;
            set => damageToHero = value;
        }

        public int DamageToEnemy
        {
            get => damageToEnemy;
            set => damageToEnemy = value;
        }
    }
}
