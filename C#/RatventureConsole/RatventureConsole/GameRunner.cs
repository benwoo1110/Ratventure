using System;
using System.Collections.Generic;
using RatventureCore;
using RatventureCore.Api;
using RatventureCore.Enums;

namespace RatventureConsole
{
    class GameRunner
    {
        private readonly IGameFactory gameFactory;

        private IGame game;
        private ConsoleHandler console;
        
        private readonly List<string> menuOptions = new List<string> { "New Game", "Resume Game", "Exit Game" };
        private readonly List<string> townOptions = new List<string> { "View Character", "View Map", "Move", "Rest", "Save Game", "Exit Game" };
        private readonly List<string> openOptions = new List<string> { "View Character", "View Map", "Move", "Sense Orb", "Exit Game" };
        private readonly List<string> attackOptions = new List<string> { "Attack", "Run" };

        public GameRunner()
        {
            gameFactory = new GameFactory();
            console = new ConsoleHandler(null);
        }

        public void Start()
        {
            while (true)
            {
                console.PrintStart();
                int menuOption = console.GetOption(menuOptions);
                switch (menuOption)
                {
                    case 1:
                        game = gameFactory.New("test player");
                        console = new ConsoleHandler(game);
                        RunGame();
                        break;
                    case 2:
                        game = gameFactory.Load();
                        console = new ConsoleHandler(game);
                        if (game != null)
                        {
                            RunGame();
                        }
                        break;
                    case 3:
                        if (console.ConfirmSelection("quit game"))
                        {
                            Environment.Exit(0);
                            return;
                        }
                        break;
                    default:
                        throw new ArgumentException("No such option: " + menuOption);
                }
            }
        }

        private void RunGame()
        {
            while (true)
            {
                if (game.HeroInTown())
                {
                    console.TellStory($"Day {game.DayCount}: You are in a town.");
                    int townOption = console.GetOption(townOptions);
                    switch (townOption)
                    {
                        case 1:
                            console.PrintHeroInfo();
                            continue;
                        case 2:
                            console.PrintGrid();
                            continue;
                        case 3:
                            Move();
                            break;
                        case 4:
                            game.HeroRest();
                            break;
                        case 5:
                            gameFactory.Save(game);
                            break;
                        case 6:
                            if (console.ConfirmSelection("exit to main menu"))
                            {
                                console.BackToMainMenu();
                                return;
                            }
                            break;
                        default:
                            throw new ArgumentException("No such option: " + townOption);
                    }
                }
                else
                {
                    console.TellStory($"Day {game.DayCount}: You are out in the open.");
                    if (game.EncounterEnemy())
                    {
                        switch (RunAttack())
                        {
                            case AttackResult.HeroLost:
                            case AttackResult.HeroWon:
                                console.BackToMainMenu();
                                return;
                        }
                    }
                    int openOption = console.GetOption(openOptions);
                    switch (openOption)
                    {
                        case 1:
                            console.PrintHeroInfo();
                            continue;
                        case 2:
                            console.PrintGrid();
                            continue;
                        case 3:
                            Move();
                            break;
                        case 4:
                            console.PrintOrbState(game.SenseOrb());
                            break;
                        case 5:
                            if (console.ConfirmSelection("exit to main menu"))
                            {
                                console.BackToMainMenu();
                                return;
                            }
                            break;
                        default:
                            throw new ArgumentException("No such option: " + openOption);
                    }
                }

                game.NextDay();
            }
        }

        private void Move()
        {
            console.PrintGrid();

            bool moved = false;
            while (!moved)
            {
                moved = game.HeroMove(console.GetMoveDirection());
                if (!moved)
                {
                    console.TellStory("You cannot move out of the map!");
                }
            }

            game.ResetEnemy();
            console.PrintGrid();
        }

        private AttackResult RunAttack()
        {
            if (game.Enemy == null)
            {
                throw new NullReferenceException("Cannot attack a null enemy!");
            }

            game.Enemy.Stats.ResetHealth();
            while (true)
            {
                console.TellStory($"Encounter! - {game.Enemy.Type}");
                console.PrintStats(game.Enemy);
                int attackOption = console.GetOption(attackOptions);
                switch (attackOption)
                {
                    case 1:
                        IAttackOutcome outcome = game.DoAttack();
                        console.PrintAttackOutcome(outcome);
                        if (!outcome.IsResult(AttackResult.EnemyStillAlive))
                        {
                            return outcome.Result;
                        }
                        break;
                    case 2:
                        console.TellStory("You ran and hide...");
                        return AttackResult.Run;
                    default:
                        throw new ArgumentException("No such option: " + attackOption);
                }
            }
        }
    }
}
