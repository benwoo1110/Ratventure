using System;
using Ratventure.Core.Api;

namespace Ratventure.Core.GamePlay
{
    [Serializable]
    class Location : ILocation
    {
        private int row;
        private int column;
        private int lowerRowLimit;
        private int upperRowLimit;
        private int lowerColumnLimit;
        private int upperColumnLimit;

        public int Row => row;

        public int Column => column;

        public int LowerRowLimit => lowerRowLimit;

        public int UpperRowLimit => upperRowLimit;

        public int LowerColumnLimit => lowerColumnLimit;

        public int UpperColumnLimit => upperColumnLimit;

        public Location()
        {
            Init(int.MinValue, int.MinValue, int.MinValue, int.MaxValue, int.MinValue, int.MaxValue);
        }

        public Location(ILocation lo)
        {
            Init(lo.Row, lo.Column, lo.LowerRowLimit, lo.UpperRowLimit, lo.LowerColumnLimit, lo.UpperColumnLimit);
        }

        public Location(int row, int column)
        {
            Init(row, column, 0, int.MaxValue, 0, int.MaxValue);
        }

        public Location(int row, int column, int lowerRowLimit, int upperRowLimit, int lowerColumnLimit, int upperColumnLimit)
        {
            Init(row, column, lowerRowLimit, upperRowLimit, lowerColumnLimit, upperColumnLimit);
        }

        private void Init(int row, int column, int lowerRowLimit, int upperRowLimit, int lowerColumnLimit, int upperColumnLimit)
        {
            this.row = row;
            this.column = column;
            this.lowerRowLimit = lowerRowLimit;
            this.upperRowLimit = upperRowLimit;
            this.lowerColumnLimit = lowerColumnLimit;
            this.upperColumnLimit = upperColumnLimit;
        }

        public bool MoveRow(int r)
        {
            return Move(r, 0);
        }

        public bool MoveColumn(int c)
        {
            return Move(0, c);
        }

        public bool Move(int r, int c)
        {
            row += r;
            column += c;
            return CheckLimits();
        }

        public int DistanceFrom(int r, int c)
        {
            return Math.Abs(row - r) + Math.Abs(column - c);
        }

        public int DistanceFrom(ILocation other)
        {
            return Math.Abs(row - other.Row) + Math.Abs(column - other.Column);
        }

        public bool Set(int r, int c)
        {
            row = r;
            column = c;
            return CheckLimits();
        }

        public bool SetLimit(int lowerRowLimit, int upperRowLimit, int lowerColumnLimit, int upperColumnLimit)
        {
            if (lowerRowLimit > upperRowLimit || lowerColumnLimit > upperColumnLimit)
            {
                throw new ArgumentException("Lower limit cannot be more than upper limit!");
            }

            this.lowerRowLimit = lowerRowLimit;
            this.upperRowLimit = upperRowLimit;
            this.lowerColumnLimit = lowerColumnLimit;
            this.upperColumnLimit = upperColumnLimit;

            return CheckLimits();
        }

        private bool CheckLimits()
        {
            bool withinLimit = true;

            if (row < lowerRowLimit)
            {
                withinLimit = false;
                row = lowerRowLimit;
            }
            else if (row > upperRowLimit)
            {
                withinLimit = false;
                row = upperRowLimit;
            }
            if (column < lowerColumnLimit)
            {
                withinLimit = false;
                column = lowerColumnLimit;
            }
            else if (column > upperColumnLimit)
            {
                withinLimit = false;
                column = upperColumnLimit;
            }

            return withinLimit;
        }

        public bool Equals(int r, int c)
        {
            return row == r && column == c;
        }

        public override bool Equals(object? o)
        {
            if (!(o is ILocation))
            {
                return false;
            }

            ILocation other = (ILocation) o;
            return row == other.Row && column == other.Column;
        }

        public string GetDirectionTo(ILocation other)
        {
            string direction = "";

            if (row > other.Row)
            {
                direction += "north";
            }
            else if (row < other.Row)
            {
                direction += "south";
            }
            if (column > other.Column)
            {
                direction += "west";
            }
            else if (column < other.Column)
            {
                direction += "east";
            }

            return direction;
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(this);
        }

        public override string ToString()
        {
            return $"r={row}, c={column}";
        }
    }
}
