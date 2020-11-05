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
        private int dayCount;
        private IGrid grid;
        private ILivingEntity hero;
        private ILivingEntity enemy;
        private List<IEntity> towns;
        private ILocation orbLocation;
        private List<ILocation> victoryLocations;

        [NonSerialized] private static readonly Random Random = new Random();
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

        public Game()
        {
            this.grid = new Grid(8, 8);
            this.towns = new List<IEntity>();
            this.victoryLocations = new List<ILocation>();

            this.dayCount = 1;
            this.grid.Clear();
            this.towns.Clear();
            this.victoryLocations.Clear();
            this.enemy = null;

            this.hero = new LivingEntity(
                EntityType.Hero,
                'H',
                new Location(0, 0),
                new Stats(2, 4, 1, 20, 20, false)
            );
            this.grid.AddEntity(hero);

            this.AddTown(new Entity(EntityType.Town, 'T', new Location(0, 0)));

            this.grid.AddEntity(new LivingEntity(
                EntityType.King,
                'K',
                new Location(grid.Rows - 1, grid.Columns - 1),
                new Stats(6, 10, 5, 24, 24, true)
            ));

            this.GenerateOrb();
            this.GenerateRandomTowns(4, 3);
        }

        private void GenerateOrb()
        {
            while (true)
            {
                int rRow = Random.Next(0, grid.Rows);
                int rColumn = Random.Next(0, grid.Rows);
                if (rRow >= 4 || rColumn >= 4)
                {
                    this.orbLocation = new Location(rRow, rColumn);
                    break;
                }
            }
        }

        private void GenerateRandomTowns(int amount, int gap)
        {
            int counter = 0;
            while (counter < amount)
            {
                int rRow = Random.Next(0, grid.Rows);
                int rColumn = Random.Next(0, grid.Rows);
                if (this.towns.Find(e => grid.HasEntityAt(rRow, rColumn) || e.GetLocation().DistanceFrom(rRow, rColumn) < gap) == null)
                {
                    this.AddTown(new Entity(EntityType.Town, 'T', new Location(rRow, rColumn)));
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
            this.towns.Add(town);
            this.grid.AddEntity(town);
        }

        public bool HeroInTown()
        {
            return towns.Find(t => t.GetLocation().Equals(hero.GetLocation())) != null;
        }

        public void HeroRest()
        {
            this.hero.GetStats().ResetHealth();
        }

        public bool HeroMove(Direction direction)
        {
            bool moved = false;

            switch (direction)
            {
                case Direction.Up:
                    moved = this.hero.GetLocation().MoveRow(-1);
                    break;
                case Direction.Left:
                    moved = this.hero.GetLocation().MoveColumn(-1);
                    break;
                case Direction.Down:
                    moved = this.hero.GetLocation().MoveRow(1);
                    break;
                case Direction.Right:
                    moved = this.hero.GetLocation().MoveColumn(1);
                    break;
                default:
                    throw new ArgumentException("Invalid direction: " + direction);
            }

            return moved;
        }

        public OrbStatus SenseOrb()
        {
            if (this.hero.GetStats().HasOrb)
            {
                return OrbStatus.AlreadyTaken;
            }

            if (this.hero.GetLocation().Equals(this.orbLocation))
            {
                this.hero.GetStats().HasOrb = true;
                this.hero.GetStats().UpdateDamage(5);
                this.hero.GetStats().UpdateDefence(5);

                return OrbStatus.Found;
            }

            return Enum.Parse<OrbStatus>(this.hero.GetLocation().GetDirectionTo(this.orbLocation), true);
        }
        public bool EncounterEnemy()
        {
            if (enemy != null && !enemy.IsDead())
            {
                return true;
            }

            if (this.victoryLocations.Find(l => l.Equals(this.hero.GetLocation())) != null)
            {
                return false;
            }

            IEntity king = this.grid.GetEntityAt(this.hero.GetLocation(), EntityType.King);
            if (king is ILivingEntity)
            {
                this.enemy = (ILivingEntity) king;
                return true;
            }

            if (Random.Next(0, 100) >= 40)
            {
                this.enemy = EnemyList[Random.Next(EnemyList.Count)];
                return true;
            }

            return false;
        }

        public IAttackOutcome DoAttack()
        {
            IAttackOutcome outcome = new AttackOutcome();

            if (!this.hero.CanDealDamageTo(this.enemy))
            {
                outcome.EnemyImmuned = true;
            }
            
            outcome.DamageToEnemy = this.hero.DealDamageTo(this.enemy);

            if (this.enemy.IsDead())
            {
                this.victoryLocations.Add(new Location(this.hero.GetLocation()));
                if (this.enemy.Type.Equals(EntityType.King))
                {
                    outcome.Result = AttackResult.HeroWon;
                    return outcome;
                }

                outcome.Result = AttackResult.EnemyDied;
                return outcome;
            }

            outcome.DamageToHero = this.enemy.DealDamageTo(this.hero);
            
            if (this.hero.IsDead())
            {
                outcome.Result = AttackResult.HeroLost;
                return outcome;
            }

            outcome.Result = AttackResult.EnemyStillAlive;
            return outcome;
        }

        public ILivingEntity GetHero()
        {
            return this.hero;
        }

        public void ResetEnemy()
        {
            this.enemy = null;
        }

        public ILivingEntity GetEnemy()
        {
            return this.enemy;
        }

        public IGrid GetGrid()
        {
            return this.grid;
        }

        public int NextDay()
        {
            return ++this.dayCount;
        }

        public int GetDay()
        {
            return this.dayCount;
        }
    }
}
