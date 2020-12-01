using Ratventure.Core.Enums;

namespace Ratventure.Core.Api
{
    public interface IEntity
    {
        EntityType Type { get; }

        char DisplayLetter { get; }

        ILocation Location { get; }

        bool Hidden { get; }
    }
}
