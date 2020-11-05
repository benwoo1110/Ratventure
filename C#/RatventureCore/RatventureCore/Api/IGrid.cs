﻿using System.Collections.Generic;
using RatventureCore.Enums;

namespace RatventureCore.Api
{
    public interface IGrid
    {
        void AddEntity(IEntity entity);

        bool HasEntityAt(int r, int c);

        IEntity GetEntityAt(ILocation location, EntityType entityType);

        IEntity GetEntityAt(int r, int c, EntityType entityType);

        List<IEntity> GetEntitiesAt(int r, int c);

        List<IEntity> GetEntitiesAt(ILocation location);

        void Clear();

        int Rows { get; }

        int Columns { get; }
    }
}