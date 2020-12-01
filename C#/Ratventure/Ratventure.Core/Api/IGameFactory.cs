using System;

namespace Ratventure.Core.Api
{
    public interface IGameFactory
    {
        ILeaderBoard LeaderBoard { get; }

        IGame New(string playerName);

        IGame Load();

        IGame Load(Guid guid);

        bool Save(IGame game);
    }
}
