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

        public Grid(int rows, int columns)
        {
            this.rows = rows;
            this.columns = columns;
            this.entityList = new List<IEntity>();
        }

        public void AddEntity(IEntity entity)
        {
            if (entity?.GetLocation() == null)
            {
                throw new ArgumentException("Invalid entity without location: " + entity);
            }
            if (!entity.GetLocation().SetLimit(0, this.Rows - 1, 0, this.Columns - 1))
            {
                throw new ArgumentException("Entity location is out of the map!");
            }

            entityList.Add(entity);
        }

        public bool HasEntityAt(int r, int c)
        {
            return entityList.Find(e => e.GetLocation().Equals(r, c)) != null;
        }

        public IEntity GetEntityAt(ILocation location, EntityType entityType)
        {
            return entityList.Find(e => e.GetLocation().Equals(location) && e.Type.Equals(entityType));
        }

        public IEntity GetEntityAt(int r, int c, EntityType entityType)
        {
            return entityList.Find(e => e.GetLocation().Equals(r, c) && e.Type.Equals(entityType));
        }

        public List<IEntity> GetEntitiesAt(int r, int c)
        {
            return entityList.FindAll(e => e.GetLocation().Equals(r, c));
        }

        public List<IEntity> GetEntitiesAt(ILocation location)
        {
            return entityList.FindAll(e => e.GetLocation().Equals(location));
        }

        public void Clear()
        {
            this.entityList.Clear();
        }

        public int Rows => rows;

        public int Columns => columns;
    }
}
