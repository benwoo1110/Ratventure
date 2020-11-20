using System;
using System.Collections.Generic;
using RatventureCore.Api;
using RatventureCore.Enums;

namespace RatventureCore.GamePlay
{
    [Serializable]
    class Grid : IGrid
    {
        private int rows;
        private int columns;
        private List<IEntity> entityList;

        public int Rows => rows;

        public int Columns => columns;

        public Grid(int r, int c)
        {
            rows = r;
            columns = c;
            entityList = new List<IEntity>();
        }

        public void AddEntity(IEntity entity)
        {
            if (entity?.Location == null)
            {
                throw new ArgumentException("Invalid entity without location: " + entity);
            }
            if (!entity.Location.SetLimit(0, Rows - 1, 0, Columns - 1))
            {
                throw new ArgumentException("Entity location is out of the map!");
            }

            entityList.Add(entity);
        }
        
        public bool HasEntityAt(ILocation location)
        {
            return HasEntityAt(location.Row, location.Column);
        }

        public bool HasEntityAt(int r, int c)
        {
            return HasEntityAt(r, c, EntityType.Any);
        }
        
        public bool HasEntityAt(ILocation location, EntityType entityType)
        {
            return HasEntityAt(location.Row, location.Column, entityType);
        }

        public bool HasEntityAt(int r, int c, EntityType entityType)
        {
            return GetEntityAt(r, c, entityType) != null;
        }

        public IEntity GetEntityAt(ILocation location)
        {
            return GetEntityAt(location.Row, location.Column);
        }

        public IEntity GetEntityAt(int r, int c)
        {
            return GetEntityAt(r, c, EntityType.Any);
        }
        
        public IEntity GetEntityAt(ILocation location, EntityType entityType)
        {
            return GetEntityAt(location.Row, location.Column, entityType);
        }

        public IEntity GetEntityAt(int r, int c, EntityType entityType)
        {
            return entityList.Find(e => EntityMatcher(e, r, c, entityType));
        }
        
        public List<IEntity> GetEntitiesAt(ILocation location)
        {
            return GetEntitiesAt(location.Row, location.Column);
        }

        public List<IEntity> GetEntitiesAt(int r, int c)
        {
            return entityList.FindAll(e => EntityMatcher(e, r, c, EntityType.Any));
        }

        public void ClearAll()
        {
            entityList.Clear();
        }

        private bool EntityMatcher(IEntity e, int r, int c, EntityType entityType)
        {
            return e.Location.Equals(r, c) 
                   && (entityType.Equals(EntityType.Any) || e.Type.Equals(entityType));
        }
    }
}
