using RatventureCore.Enums;

namespace RatventureCore.Api
{
    public interface IEntity
    {
        EntityType Type { get; }

        char DisplayLetter { get; }

        ILocation Location { get; }

        bool Hidden { get; }
    }
}
