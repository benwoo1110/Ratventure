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
            this.gameFactory = new GameFactory();
            this.console = new ConsoleHandler(null);
        }

        public void Start()
        {
            while (true)
            {
                this.console.PrintStart();
                int menuOption = this.console.GetOption(this.menuOptions);
                switch (menuOption)
                {
                    case 1:
                        this.game = this.gameFactory.New();
                        this.console = new ConsoleHandler(game);
                        this.RunGame();
                        break;
                    case 2:
                        this.game = this.gameFactory.Load();
                        this.console = new ConsoleHandler(game);
                        if (this.game != null)
                        {
                            this.RunGame();
                        }
                        break;
                    case 3:
                        if (this.console.ConfirmSelection("quit game"))
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
                    this.console.TellStory($"Day {game.GetDay()}: You are in a town.");
                    int townOption = console.GetOption(townOptions);
                    switch (townOption)
                    {
                        case 1:
                            this.console.PrintHeroInfo();
                            continue;
                        case 2:
                            this.console.PrintGrid();
                            continue;
                        case 3:
                            this.Move();
                            break;
                        case 4:
                            this.game.HeroRest();
                            break;
                        case 5:
                            this.gameFactory.Save(game);
                            break;
                        case 6:
                            if (this.console.ConfirmSelection("exit to main menu"))
                            {
                                this.console.BackToMainMenu();
                                return;
                            }
                            break;
                        default:
                            throw new ArgumentException("No such option: " + townOption);
                    }
                }
                else
                {
                    this.console.TellStory($"Day {game.GetDay()}: You are out in the open.");
                    if (game.EncounterEnemy())
                    {
                        switch (this.RunAttack())
                        {
                            case AttackResult.HeroLost:
                            case AttackResult.HeroWon:
                                this.console.BackToMainMenu();
                                return;
                        }
                    }
                    int openOption = console.GetOption(openOptions);
                    switch (openOption)
                    {
                        case 1:
                            this.console.PrintHeroInfo();
                            continue;
                        case 2:
                            this.console.PrintGrid();
                            continue;
                        case 3:
                            this.Move();
                            break;
                        case 4:
                            this.console.PrintOrbState(game.SenseOrb());
                            break;
                        case 5:
                            if (this.console.ConfirmSelection("exit to main menu"))
                            {
                                this.console.BackToMainMenu();
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
            this.console.PrintGrid();

            bool moved = false;
            while (!moved)
            {
                moved = this.game.HeroMove(this.console.GetMoveDirection());
                if (!moved)
                {
                    console.TellStory("You cannot move out of the map!");
                }
            }

            game.ResetEnemy();
            this.console.PrintGrid();
        }

        private AttackResult RunAttack()
        {
            if (game.GetEnemy() == null)
            {
                throw new NullReferenceException("Cannot attack a null enemy!");
            }

            game.GetEnemy().GetStats().ResetHealth();
            while (true)
            {
                this.console.TellStory($"Encounter! - {game.GetEnemy().Type}");
                this.console.PrintStats(game.GetEnemy());
                int attackOption = this.console.GetOption(attackOptions);
                switch (attackOption)
                {
                    case 1:
                        IAttackOutcome outcome = game.DoAttack();
                        this.console.PrintAttackOutcome(outcome);
                        if (!outcome.IsResult(AttackResult.EnemyStillAlive))
                        {
                            return outcome.Result;
                        }
                        break;
                    case 2:
                        this.console.TellStory("You ran and hide...");
                        return AttackResult.Run;
                    default:
                        throw new ArgumentException("No such option: " + attackOption);
                }
            }
        }
    }
}
