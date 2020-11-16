using System;
using System.Collections.Generic;
using System.Text;
using RatventureCore.Api;
using RatventureCore.Enums;

namespace RatventureConsole
{
    class ConsoleHandler
    {
        private IGame game;

        public ConsoleHandler(IGame game)
        {
            this.game = game;
        }

        public int GetOption(List<string> options)
        {
            PrintOptions(options);
            string invalidMessage = $"Please enter a number from 1-{options.Count}!";
            while (true)
            {
                int input = GetInput("Enter choice: ", Convert.ToInt32, invalidMessage);
                if (input > 0 && input <= options.Count)
                {
                    return input;
                }
                Console.WriteLine(invalidMessage);
            }
        }

        public Direction GetMoveDirection()
        {
            Console.WriteLine("W = up; A = left; S = down; D = right");
            return GetInput("You move: ", ParseMoveDirection, "Invalid direction! Please enter W, A, S or D.");
        }

        private Direction ParseMoveDirection(string direction)
        {
            switch (direction.ToUpper())
            {
                case "W":
                    return Direction.Up;
                case "A":
                    return Direction.Left;
                case "S":
                    return Direction.Down;
                case "D":
                    return Direction.Right;
                default:
                    throw new ArgumentException("No such direction: " + direction.ToUpper());
            }
        }

        public bool ConfirmSelection(string action)
        {
            return GetInput($"Are you sure you want to {action}? [y/n] ", Convert.ToString, "So... yea or no?")
                .ToUpper()
                .Equals("Y");
        }

        public void BackToMainMenu()
        {
            Console.Write("Game Ended! Press enter to continue...");
            Console.ReadLine();
            Console.WriteLine();
        }

        private T GetInput<T>(string prompt, Func<string, T> converter, string invalidMessage)
        {
           while (true)
           {
               try
               {
                   Console.Write(prompt);
                   return converter(Console.ReadLine());
               }
               catch (Exception)
               {
                   Console.WriteLine(invalidMessage);
               }
           }
        }
        private void PrintOptions(List<string> options)
        {
            int count = 1;
            foreach (string option in options)
            {
                Console.WriteLine("{0}) {1}", count, option);
                count++;
            }
        }

        public void PrintStart()
        {
            Console.WriteLine("Welcome to Ratventure!");
            Console.WriteLine("----------------------");
        }

        public void PrintGrid()
        {
            Console.WriteLine("+---+---+---+---+---+---+---+---+");
            for (int r = 0; r < game.Grid.Rows; r++)
            {
                StringBuilder row = new StringBuilder("|");
                for (int c = 0; c < game.Grid.Columns; c++)
                {
                    string tileText = "";
                    List<IEntity> entities = game.Grid.GetEntitiesAt(r, c);
                    if (entities != null)
                    {
                        foreach (IEntity entity in entities)
                        {
                            if (entity.Hidden)
                            {
                                continue;
                            }

                            if (!tileText.Equals(""))
                            {
                                tileText += "/";
                            }

                            tileText += entity.DisplayLetter;
                        }
                    }

                    row.Append(CenterText(tileText, 3)).Append("|");
                }

                Console.WriteLine(row.ToString());
                Console.WriteLine("+---+---+---+---+---+---+---+---+");
            }
        }

        public void PrintHeroInfo()
        {
            Console.WriteLine("--The Hero--");
            PrintStats(game.Hero);
        }

        public void PrintStats(ILivingEntity livingEntity)
        {
            PrintStats(livingEntity.Stats, false);
        }

        public void PrintStats(ILivingEntity livingEntity, bool showOrb)
        {
           PrintStats(livingEntity.Stats, showOrb);
        }

        public void PrintStats(IStats stats, bool showOrb)
        {
            Console.WriteLine("Damage: {0}-{1}", stats.MinDamage, stats.MaxDamage);
            Console.WriteLine("Defence: {0}", stats.Defence);
            Console.WriteLine("Health: {0}/{1}", stats.CurrentHealth, stats.MaxHealth);
            if (showOrb && stats.HasOrb)
            {
                Console.WriteLine("You have the orb of power!");
            }
        }

        public void PrintOrbState(OrbStatus state)
        {
            switch (state)
            {
                case OrbStatus.AlreadyTaken:
                    Console.WriteLine("You already have the OrbStatus of Power!");
                    break;
                case OrbStatus.Found:
                    Console.WriteLine("You found the OrbStatus of Power!");
                    Console.WriteLine("Your attack increases by 5!");
                    Console.WriteLine("Your defence increases by 5!");
                    break;
                case OrbStatus.North:
                case OrbStatus.South:
                case OrbStatus.East:
                case OrbStatus.West:
                case OrbStatus.NorthEast:
                case OrbStatus.NorthWest:
                case OrbStatus.SouthEast:
                case OrbStatus.SouthWest:
                    Console.WriteLine($"You sense that the OrbStatus of Power is to the {state}.");
                    break;
                default:
                    throw new ArgumentException("Invalid Orb State: " + state);
            }
        }

        public void PrintAttackOutcome(IAttackOutcome outcome)
        {
            if (outcome.EnemyImmuned)
            {
                Console.WriteLine($"You do not have the OrbStatus of Power - the {game.Enemy.Type} is immune!");
            }

            Console.WriteLine($"You deal {outcome.DamageToEnemy} damage to the {game.Enemy.Type}");

            if (outcome.IsResult(AttackResult.EnemyDied))
            {
                Console.WriteLine($"The {game.Enemy.Type} is dead! You are victorious!");
            }
            if (outcome.IsResult(AttackResult.HeroWon))
            {
                Console.WriteLine("Congratulations, you have defeated the Rat King!");
                Console.WriteLine("You have saved the world from tragedy! Great Job!");
                return;
            }

            Console.WriteLine($"Ouch! The  {game.Enemy.Type} hit you for {outcome.DamageToHero} damage!");

            if (outcome.IsResult(AttackResult.HeroLost))
            {
                Console.WriteLine($"Oh no! You were defeated by {game.Enemy.Type}...");
                Console.WriteLine("Game Over.");
                return;
            }

            if (outcome.IsResult(AttackResult.EnemyStillAlive))
            {
                Console.WriteLine($"You have {game.Enemy.Stats.CurrentHealth} health left.");
            }
        }

        public void TellStory(string story)
        {
            Console.WriteLine($"\n{story}");
        }

        private string CenterText(string text, int spacing)
        {
            if (text.Length == 0)
            {
                return new string(' ', spacing);
            }
            if (text.Length >= spacing)
            {
                return text;
            }
            StringBuilder newText = new StringBuilder();
            int beforeSpaces = (spacing - text.Length) / 2;
            return newText
                .Append(new string(' ', beforeSpaces))
                .Append(text)
                .Append(new string(' ', spacing - text.Length - beforeSpaces))
                .ToString();
        }
    }
}
