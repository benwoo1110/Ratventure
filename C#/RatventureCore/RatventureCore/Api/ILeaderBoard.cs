using System;
using System.Collections.Generic;
using System.Text;

namespace RatventureCore.Api
{
    public interface ILeaderBoard
    {
        bool AddGameResult(string playerName, int dayCount);

        bool AddGameResult(IGame game);

        IEnumerable<IBoardItem> GetTopFive();
    }
}
