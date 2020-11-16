using System;
using RatventureCore;
using RatventureCore.Api;

namespace RatventureConsole
{
    class Program
    {
        static void Main(string[] args)
        {
            IGameFactory game = new GameFactory();
            game.AddGameResult("z", 29);
            game.AddGameResult("a", 29);
            game.AddGameResult("3", 30);
            game.AddGameResult("4", 40);
            game.AddGameResult("5", 42);
            game.AddGameResult("6", 60);

            foreach (IBoardItem board in game.GetTopFive())
            {
                Console.WriteLine(board);
            }

            game.New("Ben");
            game.New("Woo");
        }
    }
}
