using System;
using System.Collections.Generic;
using System.Data;

namespace RatventureCore.Api
{
    public interface IBoardItem : IComparable<IBoardItem>
    {
        string PlayerName { get; }

        int DayCount { get; }

        DateTime TimeAdded { get; } 
    }
}