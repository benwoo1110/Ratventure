namespace RatventureCore.Api
{
    public interface ILocation
    {
        int Row { get; }

        int Column { get; }

        int LowerRowLimit { get; }

        int UpperRowLimit { get; }

        int LowerColumnLimit { get; }

        int UpperColumnLimit { get; }

        bool MoveRow(int r);

        bool MoveColumn(int c);

        bool Move(int r, int c);

        int DistanceFrom(int r, int c);

        int DistanceFrom(ILocation other);

        bool Set(int r, int c);

        bool SetLimit(int lowerRowLimit, int upperRowLimit, int lowerColumnLimit, int upperColumnLimit);

        bool Equals(int row, int column);

        bool Equals(object? o);

        public string GetDirectionTo(ILocation other);

        int GetHashCode();

        string ToString();
    }
}
