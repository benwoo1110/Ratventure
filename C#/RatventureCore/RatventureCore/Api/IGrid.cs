using System.Collections.Generic;
using RatventureCore.Enums;
using RatventureCore.GamePlay;

namespace RatventureCore.Api
{
    public interface IGrid
    {
        int Rows { get; }

        int Columns { get; }
        
        void AddEntity(IEntity entity);

        bool HasEntityAt(ILocation location);

        bool HasEntityAt(int r, int c);

        bool HasEntityAt(ILocation location, EntityType entityType);

        bool HasEntityAt(int r, int c, EntityType entityType);

        IEntity GetEntityAt(ILocation location);

        IEntity GetEntityAt(int r, int c);
        
        IEntity GetEntityAt(ILocation location, EntityType entityType);

        IEntity GetEntityAt(int r, int c, EntityType entityType);

        List<IEntity> GetEntitiesAt(ILocation location);
        
        List<IEntity> GetEntitiesAt(int r, int c);

        void ClearAll();
    }
}
