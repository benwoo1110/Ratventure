using System;
using RatventureCore.Api;
using RatventureCore.Enums;

namespace RatventureCore.GamePlay
{
    [Serializable]
    class LivingEntity : Entity, ILivingEntity
    {
        private IStats stats;

        public IStats Stats => stats;

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

            int damageDone = stats.GetRandomDamage() - enemy.Stats.Defence;
            damageDone = (damageDone < 0) ? 0 : damageDone;
            enemy.Stats.UpdateHealth(-damageDone);
            return damageDone;
        }

        public bool CanDealDamageTo(ILivingEntity enemy)
        {
            return stats.HasOrb || !enemy.Stats.HasOrb;
        }

        public bool IsDead()
        {
            return stats.CurrentHealth <= 0;
        }
    }
}
