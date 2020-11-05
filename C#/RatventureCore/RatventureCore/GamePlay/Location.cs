using System;
using RatventureCore.Api;

namespace RatventureCore.GamePlay
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

        public Location(ILocation lo)
        {
            Init(lo.Row, lo.Column, lo.LowerRowLimit, lo.UpperRowLimit, lo.LowerColumnLimit, lo.UpperColumnLimit);
        }

        public Location(int row, int column)
        {
            Init(row, column, 0, Int32.MaxValue, 0, Int32.MaxValue);
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
            return this.Move(r, 0);
        }

        public bool MoveColumn(int c)
        {
            return this.Move(0, c);
        }

        public bool Move(int r, int c)
        {
            this.row += r;
            this.column += c;
            return this.CheckLimits();
        }

        public int DistanceFrom(int r, int c)
        {
            return Math.Abs(this.row - r) + Math.Abs(this.column - c);
        }

        public int DistanceFrom(ILocation other)
        {
            return Math.Abs(this.row - other.Row) + Math.Abs(this.column - other.Column);
        }

        public bool Set(int r, int c)
        {
            this.row = r;
            this.column = c;
            return this.CheckLimits();
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

            return this.CheckLimits();
        }

        private bool CheckLimits()
        {
            bool withinLimit = true;
            if (this.row < this.lowerRowLimit)
            {
                withinLimit = false;
                this.row = this.lowerRowLimit;
            }
            else if (this.row > this.upperRowLimit)
            {
                withinLimit = false;
                this.row = upperRowLimit;
            }
            if (this.column < this.lowerColumnLimit)
            {
                withinLimit = false;
                this.column = lowerColumnLimit;
            }
            else if (this.column > this.upperColumnLimit)
            {
                withinLimit = false;
                this.column = upperColumnLimit;
            }

            return withinLimit;
        }

        public bool Equals(int row, int column)
        {
            return this.row == row && this.column == column;
        }

        public override bool Equals(object? o)
        {
            if (!(o is ILocation))
            {
                return false;
            }

            ILocation other = (ILocation) o;
            return this.row == other.Row && this.column == other.Column;
        }

        public string GetDirectionTo(ILocation other)
        {
            string direction = "";

            if (this.row > other.Row)
            {
                direction += "north";
            }
            else if (this.row < other.Row)
            {
                direction += "south";
            }
            if (this.column > other.Column)
            {
                direction += "west";
            }
            else if (this.column < other.Column)
            {
                direction += "east";
            }

            return direction;
        }

        public int Row => row;

        public int Column => column;

        public int LowerRowLimit => lowerRowLimit;

        public int UpperRowLimit => upperRowLimit;

        public int LowerColumnLimit => lowerColumnLimit;

        public int UpperColumnLimit => upperColumnLimit;

        public override int GetHashCode()
        {
            return HashCode.Combine(this);
        }

        public override string ToString()
        {
            return $"r={this.row}, c={this.column}";
        }
    }
}
