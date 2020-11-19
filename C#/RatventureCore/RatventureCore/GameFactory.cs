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
        private readonly ILeaderBoard leaderBoard;
        private readonly Dictionary<Guid, IGame> cachedSaves;

        public ILeaderBoard LeaderBoard => leaderBoard;

        public GameFactory()
        {
            leaderBoard = new LeaderBoard();
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
    }
}
