using System;

namespace Ratventure.Core.Api
{
    public interface IBoardItem : IComparable<IBoardItem>
    {
        string PlayerName { get; }

        int DayCount { get; }

        DateTime TimeAdded { get; } 
    }
}