using RatventureCore.Enums;

namespace RatventureCore.Api
{
    public interface IGame
    {
        bool HeroInTown();

        void HeroRest();

        bool HeroMove(Direction direction);

        OrbStatus SenseOrb();

        bool EncounterEnemy();

        IAttackOutcome DoAttack();

        ILivingEntity GetHero();

        void ResetEnemy();

        ILivingEntity GetEnemy();

        IGrid GetGrid();

        int NextDay();

        int GetDay();
    }
}
