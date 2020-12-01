using System.Collections.Generic;
using System.Linq;
using Ratventure.Core.Api;
using Ratventure.Core.GamePlay;

namespace Ratventure.Core
{
    class LeaderBoard : ILeaderBoard
    {
        private static readonly string LeaderBoardFileName = @"leaderboard.bin";

        private readonly SortedSet<IBoardItem> scores;

        public LeaderBoard()
        {
            scores = LoadLeaderBoard();
        }

        public bool AddGameResult(string playerName, int dayCount)
        {
            scores.Add(new BoardItem(playerName, dayCount));
            return SaveLeaderBoard();
        }

        public bool AddGameResult(IGame game)
        {
            scores.Add(new BoardItem(game));
            return SaveLeaderBoard();
        }

        public IEnumerable<IBoardItem> GetTopFive()
        {
            return scores.ToList().GetRange(0, 5);
        }

        private SortedSet<IBoardItem> LoadLeaderBoard()
        {
            return (SortedSet<IBoardItem>)RatUtils.LoadFile(LeaderBoardFileName) ?? new SortedSet<IBoardItem>();
        }

        private bool SaveLeaderBoard()
        {
            return RatUtils.SaveFile(LeaderBoardFileName, scores);
        }
    }
}
