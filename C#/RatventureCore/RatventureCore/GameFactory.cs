using System;
using System.Collections.Generic;
using System.Data.Common;
using System.IO;
using System.Linq;
using System.Runtime.Serialization.Formatters.Binary;
using RatventureCore.Api;
using RatventureCore.GamePlay;

namespace RatventureCore
{
    public class GameFactory : IGameFactory
    {
        private readonly SortedSet<IBoardItem> leaderBoard;
        private readonly Dictionary<Guid, IGame> cachedSaves;

        private static readonly string LeaderBoardFileName = @"leaderboard.bin";

        public GameFactory()
        {
            leaderBoard = LoadLeaderBoard();
            cachedSaves = new Dictionary<Guid, IGame>();
        }

        public IGame New(string playerName)
        {
            return new Game(playerName);
        }

        public IGame Load(Guid guid)
        {
            return (IGame) RatUtils.LoadFile(ParseSaveName(guid));
        }

        public bool Save(IGame game)
        {
            return RatUtils.SaveFile(ParseSaveName(game.Guid), game);
        }

        private string ParseSaveName(Guid guid)
        {
            return @$"{guid}.bin";
        }

        public bool AddGameResult(string playerName, int dayCount)
        {
            leaderBoard.Add(new BoardItem(playerName, dayCount));
            return SaveLeaderBoard();
        }

        public bool AddGameResult(IGame game)
        {
            leaderBoard.Add(new BoardItem(game));
            return SaveLeaderBoard();
        }

        public IEnumerable<IBoardItem> GetTopFive()
        {
            return leaderBoard.ToList().GetRange(0, 5);
        }

        private SortedSet<IBoardItem> LoadLeaderBoard()
        {
            return (SortedSet<IBoardItem>) RatUtils.LoadFile(LeaderBoardFileName) ?? new SortedSet<IBoardItem>();
        }

        private bool SaveLeaderBoard()
        {
            return RatUtils.SaveFile(LeaderBoardFileName, leaderBoard);
        }
    }
}
