using RatventureCore.Enums;

namespace RatventureCore.Api
{
    public interface IGame
    {
        int DayCount { get; }

        IGrid Grid { get; }

        ILivingEntity Hero { get; }

        ILivingEntity Enemy { get; }

        bool HeroInTown();

        void HeroRest();

        bool HeroMove(Direction direction);

        OrbStatus SenseOrb();

        bool EncounterEnemy();

        IAttackOutcome DoAttack();

        void ResetEnemy();

        int NextDay();
    }
}
