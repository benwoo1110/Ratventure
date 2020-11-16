using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using RatventureCore.Api;
using RatventureCore.Enums;

namespace RatventureCore.GamePlay
{
    [Serializable]
    class Game : IGame
    {
        private readonly Guid guid;

        private string playerName;
        private int dayCount;
        private IGrid grid;
        private ILivingEntity hero;
        private ILivingEntity enemy;
        private List<IEntity> towns;
        private ILocation orbLocation;
        private List<ILocation> victoryLocations;

        [NonSerialized] private static readonly List<ILivingEntity> EnemyList = new List<ILivingEntity>
        {
            new LivingEntity(
                EntityType.Enemy, 'F', null,
                new Stats(1, 3, 1, 6, 6, false)
                ),
            new LivingEntity(
                EntityType.Enemy, 'R', null, 
                new Stats(1, 3, 1, 8, 8, false)
                ),
            new LivingEntity(
                EntityType.Enemy, 'C', null,
                new Stats(2, 3, 1, 10, 10, false)
                )
        };

        public Guid Guid => guid;

        public string PlayerName => playerName;

        public int DayCount => dayCount;

        public IGrid Grid => grid;

        public ILivingEntity Hero => hero;

        public ILivingEntity Enemy => enemy;

        public Game(string player)
        {
            guid = Guid.NewGuid();

            playerName = player;
            dayCount = 1;
            grid = new Grid(8, 8);
            towns = new List<IEntity>();
            victoryLocations = new List<ILocation>();

            hero = new LivingEntity(
                EntityType.Hero, 'H', new Location(0, 0),
                new Stats(2, 4, 1, 20, 20, false)
            );
            grid.AddEntity(hero);

            AddTown(new Entity(EntityType.Town, 'T', new Location(0, 0)));

            grid.AddEntity(new LivingEntity(
                EntityType.King, 'K', new Location(grid.Rows - 1, grid.Columns - 1),
                new Stats(6, 10, 5, 24, 24, true)
            ));

            GenerateOrb();
            GenerateRandomTowns(4, 3);
        }

        private void GenerateOrb()
        {
            while (true)
            {
                int rRow = RatUtils.RandomNumber(0, grid.Rows);
                int rColumn = RatUtils.RandomNumber(0, grid.Rows);
                if (rRow >= 4 || rColumn >= 4)
                {
                    orbLocation = new Location(rRow, rColumn);
                    break;
                }
            }
        }

        private void GenerateRandomTowns(int amount, int gap)
        {
            int counter = 0;
            while (counter < amount)
            {
                int rRow = RatUtils.RandomNumber(0, grid.Rows);
                int rColumn = RatUtils.RandomNumber(0, grid.Rows);
                if (towns.Find(e => grid.HasEntityAt(rRow, rColumn) || e.Location.DistanceFrom(rRow, rColumn) < gap) == null)
                {
                    AddTown(new Entity(EntityType.Town, 'T', new Location(rRow, rColumn)));
                    counter++;
                }
            }
        }

        private void AddTown(IEntity town)
        {
            if (!town.Type.Equals(EntityType.Town))
            {
                throw new ArgumentException("Invalid town!");
            }
            towns.Add(town);
            grid.AddEntity(town);
        }

        public bool HeroInTown()
        {
            return towns.Find(t => t.Location.Equals(hero.Location)) != null;
        }

        public void HeroRest()
        {
            hero.Stats.ResetHealth();
        }

        public bool HeroMove(Direction direction)
        {
            switch (direction)
            {
                case Direction.Up:
                    return hero.Location.MoveRow(-1);
                case Direction.Left:
                    return hero.Location.MoveColumn(-1);
                case Direction.Down:
                    return hero.Location.MoveRow(1);
                case Direction.Right:
                    return hero.Location.MoveColumn(1);
                default:
                    throw new ArgumentException("Invalid direction: " + direction);
            }
        }

        public OrbStatus SenseOrb()
        {
            if (hero.Stats.HasOrb)
            {
                return OrbStatus.AlreadyTaken;
            }

            if (hero.Location.Equals(orbLocation))
            {
                hero.Stats.HasOrb = true;
                hero.Stats.UpdateDamage(5);
                hero.Stats.UpdateDefence(5);

                return OrbStatus.Found;
            }

            return Enum.Parse<OrbStatus>(hero.Location.GetDirectionTo(orbLocation), true);
        }
        public bool EncounterEnemy()
        {
            if (enemy != null && !enemy.IsDead())
            {
                return true;
            }

            if (victoryLocations.Find(l => l.Equals(hero.Location)) != null)
            {
                return false;
            }

            IEntity king = grid.GetEntityAt(hero.Location, EntityType.King);
            if (king is ILivingEntity)
            {
                enemy = (ILivingEntity) king;
                return true;
            }

            if (RatUtils.RandomNumber(0, 100) >= 40)
            {
                enemy = EnemyList[RatUtils.RandomNumber(0, EnemyList.Count)];
                return true;
            }

            return false;
        }

        public IAttackOutcome DoAttack()
        {
            AttackOutcome outcome = new AttackOutcome();

            outcome.EnemyImmuned = !hero.CanDealDamageTo(enemy);

            outcome.DamageToEnemy = hero.DealDamageTo(enemy);

            if (enemy.IsDead())
            {
                victoryLocations.Add(new Location(hero.Location));
                outcome.Result = (enemy.Type.Equals(EntityType.King)) ? AttackResult.HeroWon : AttackResult.EnemyDied;
                return outcome;
            }

            outcome.DamageToHero = enemy.DealDamageTo(hero);

            outcome.Result = (hero.IsDead()) ? AttackResult.HeroLost : AttackResult.EnemyStillAlive;
            return outcome;
        }

        public void ResetEnemy()
        {
            enemy = null;
        }

        public int NextDay()
        {
            return ++dayCount;
        }

    }
}
