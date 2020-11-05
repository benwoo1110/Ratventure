using System;
using RatventureCore.Api;

namespace RatventureCore.GamePlay
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
        
        [NonSerialized] private static readonly Random random = new Random();

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
            return random.Next(this.minDamage, this.maxDamage+1);
        }

        public void UpdateDamage(int by)
        {
            this.minDamage += by;
            this.maxDamage += by;
        }

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

        public void UpdateDefence(int by)
        {
            this.defence += by;
        }

        public int Defence
        {
            get => defence;
            set => defence = value;
        }

        public void ResetHealth()
        {
            this.currentHealth = this.maxHealth;
        }

        public void UpdateHealth(int by)
        {
            this.currentHealth += by;
            this.ValidateNewHealth();
        }

        public int CurrentHealth
        {
            get => currentHealth;
            set
            {
                currentHealth = value;
                this.ValidateNewHealth();
            }
        }

        public int MaxHealth
        {
            get => maxHealth;
            set
            {
                maxHealth = value;
                this.ValidateNewHealth();
            }
        }

        private void ValidateNewHealth()
        {
            if (this.maxHealth < 0)
            {
                this.maxHealth = 0;
                this.currentHealth = 0;
                throw new ArgumentException("Max health must be a non-negative number!");
            }
            if (this.currentHealth > this.maxHealth)
            {
                this.currentHealth = this.maxHealth;
                throw new ArgumentException("Current health cannot be more that max health!");
            }
        }

        public bool HasOrb
        {
            get => hasOrb;
            set => hasOrb = value;
        }
    }
}