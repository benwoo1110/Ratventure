namespace RatventureCore.Api
{
    public interface IStats
    {
        int GetRandomDamage();

        void UpdateDamage(int by);

        int MinDamage { get; set; }

        int MaxDamage { get; set; }

        void UpdateDefence(int by);

        int Defence { get; set; }

        void ResetHealth();

        void UpdateHealth(int by);

        int CurrentHealth { get; set; }

        int MaxHealth { get; set; }

        bool HasOrb { get; set; }
    }
}
