using RatventureCore.Enums;

namespace RatventureCore.Api
{
    public interface IEntity
    {
        ILocation GetLocation();

        EntityType Type { get; }

        char DisplayLetter { get; }

        bool Hidden { get; }
    }
}
