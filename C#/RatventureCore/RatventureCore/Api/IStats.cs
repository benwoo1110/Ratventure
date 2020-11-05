namespace RatventureCore.Api
{
    public interface IStats
    {
        int MinDamage { get; set; }

        int MaxDamage { get; set; }

        int Defence { get; set; }

        int CurrentHealth { get; set; }

        int MaxHealth { get; set; }

        bool HasOrb { get; set; }

        int GetRandomDamage();

        void UpdateDamage(int by);

        void UpdateDefence(int by);

        void ResetHealth();

        void UpdateHealth(int by);
    }
}
