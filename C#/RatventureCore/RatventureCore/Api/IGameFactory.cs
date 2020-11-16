using System;
using System.Collections.Generic;

namespace RatventureCore.Api
{
    public interface IGameFactory
    {
        IGame New(string playerName);

        IGame Load(Guid guid);

        bool Save(IGame game);

        bool AddGameResult(string playerName, int dayCount);

        bool AddGameResult(IGame game);

        IEnumerable<IBoardItem> GetTopFive();
    }
}
