using System;
using Ratventure.Core.Api;

namespace Ratventure.Core.GamePlay
{
    [Serializable]
    class BoardItem : IBoardItem
    {
        private readonly string playerName;
        private readonly int dayCount;
        private readonly DateTime timeAdded;

        public string PlayerName => playerName;

        public int DayCount => dayCount;

        public DateTime TimeAdded => timeAdded;

        public BoardItem(IGame game)
        {
            playerName = game.PlayerName;
            dayCount = game.DayCount;
            timeAdded = DateTime.Now;
        }

        public BoardItem(string playerName, int dayCount)
        {
            this.playerName = playerName;
            this.dayCount = dayCount;
            timeAdded = DateTime.Now;
        }

        public int CompareTo(IBoardItem other)
        {
            if (dayCount != other.DayCount)
            {
                return dayCount - other.DayCount;
            }
            if (!timeAdded.Equals(other.TimeAdded))
            {
                return timeAdded.CompareTo(other.TimeAdded);
            }

            return string.CompareOrdinal(playerName, other.PlayerName);
        }

        public override string ToString()
        {
            return $"playerName:{playerName}\tdayCount:{dayCount}\tgameTime:{TimeAdded}";
        }
    }
}
