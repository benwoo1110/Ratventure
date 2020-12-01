using System;
using Ratventure.Core.Api;

namespace Ratventure.Core.GamePlay
{
    [Serializable]
    class Stats : IStats
    {
        private int minDamage;
        private int maxDamage;
        private int defence;
        private int currentHealth;
        private int maxHealth;
        private bool hasOrb;
        
        public int MinDamage
        {
            get => minDamage;
            set => minDamage = value;
        }

        public int MaxDamage
        {
            get => maxDamage;
            set => maxDamage = value;
        }

        public int Defence
        {
            get => defence;
            set => defence = value;
        }

        public int CurrentHealth
        {
            get => currentHealth;
            set
            {
                currentHealth = value;
                ValidateNewHealth();
            }
        }

        public int MaxHealth
        {
            get => maxHealth;
            set
            {
                maxHealth = value;
                ValidateNewHealth();
            }
        }

        public bool HasOrb
        {
            get => hasOrb;
            set => hasOrb = value;
        }

        public Stats(int minDamage, int maxDamage, int defence, int currentHealth, int maxHealth, bool hasOrb)
        {
            this.minDamage = minDamage;
            this.maxDamage = maxDamage;
            this.defence = defence;
            this.currentHealth = currentHealth;
            this.maxHealth = maxHealth;
            this.hasOrb = hasOrb;
        }

        public int GetRandomDamage()
        {
            return RatUtils.RandomNumber(minDamage, maxDamage+1);
        }

        public void UpdateDamage(int by)
        {
            minDamage += by;
            maxDamage += by;
        }

        public void UpdateDefence(int by)
        {
            defence += by;
        }

        public void UpdateHealth(int by)
        {
            currentHealth += by;
            ValidateNewHealth();
        }

        public void ResetHealth()
        {
            currentHealth = maxHealth;
        }

        private void ValidateNewHealth()
        {
            if (maxHealth < 0)
            {
                maxHealth = 0;
                currentHealth = 0;
                throw new ArgumentException("Max health must be a non-negative number!");
            }
            if (currentHealth > maxHealth)
            {
                currentHealth = maxHealth;
                throw new ArgumentException("Current health cannot be more that max health!");
            }
        }
    }
}