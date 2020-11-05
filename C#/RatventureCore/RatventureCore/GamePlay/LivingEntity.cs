using System;
using RatventureCore.Api;
using RatventureCore.Enums;

namespace RatventureCore.GamePlay
{
    [Serializable]
    class LivingEntity : Entity, ILivingEntity
    {
        private IStats stats;

        public LivingEntity(EntityType type, char displayLetter, ILocation location, IStats stats)
            : base(type, displayLetter, location)
        {
            this.stats = stats;
        }

        public int DealDamageTo(ILivingEntity enemy)
        {
            if (!CanDealDamageTo(enemy))
            {
                return 0;
            }

            int damageDone = this.stats.GetRandomDamage() - enemy.GetStats().Defence;
            damageDone = (damageDone < 0) ? 0 : damageDone;
            enemy.GetStats().UpdateHealth(-damageDone);
            return damageDone;
        }

        public bool CanDealDamageTo(ILivingEntity enemy)
        {
            return this.stats.HasOrb || !enemy.GetStats().HasOrb;
        }

        public bool IsDead()
        {
            return stats.CurrentHealth <= 0;
        }

        public IStats GetStats()
        {
            return this.stats;
        }
    }
}
