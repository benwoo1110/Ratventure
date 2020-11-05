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

        public AttackOutcome()
        {
            result = AttackResult.Unknown;
            enemyImmuned = false;
            damageToHero = 0;
            damageToEnemy = 0;
        }

        public AttackOutcome(AttackResult result, bool enemyImmuned, int damageToHero, int damageToEnemy)
        {
            this.result = result;
            this.enemyImmuned = enemyImmuned;
            this.damageToHero = damageToHero;
            this.damageToEnemy = damageToEnemy;
        }
    }
}
