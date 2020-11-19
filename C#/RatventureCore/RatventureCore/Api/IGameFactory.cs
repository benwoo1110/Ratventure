using System;
using System.Collections.Generic;

namespace RatventureCore.Api
{
    public interface IGameFactory
    {
        ILeaderBoard LeaderBoard { get; }

        IGame New(string playerName);

        IGame Load(Guid guid);

        bool Save(IGame game);
    }
}
