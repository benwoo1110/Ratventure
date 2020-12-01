using System;
using Ratventure.Core.Enums;

namespace Ratventure.Core.Api
{
    public interface IGame
    {
        Guid Guid { get; }

        string PlayerName { get; }

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
