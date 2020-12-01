using System.Collections.Generic;

namespace Ratventure.Core.Api
{
    public interface ILeaderBoard
    {
        bool AddGameResult(string playerName, int dayCount);

        bool AddGameResult(IGame game);

        IEnumerable<IBoardItem> GetTopFive();
    }
}
