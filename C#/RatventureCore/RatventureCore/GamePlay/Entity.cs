﻿using System;
using RatventureCore.Api;
using RatventureCore.Enums;

namespace RatventureCore.GamePlay
{
    [Serializable]
    class Entity : IEntity
    {
        private EntityType type;
        private char displayLetter;
        private ILocation location;
        private bool hidden;

        public Entity(EntityType type, char displayLetter, ILocation location)
        {
            Init(type, displayLetter, location, false);
        }

        public Entity(EntityType name, char displayLetter, ILocation location, bool hidden)
        {
            Init(type, displayLetter, location, hidden);
        }

        private void Init(EntityType type, char displayLetter, ILocation location, bool hidden)
        {
            this.type = type;
            this.displayLetter = displayLetter;
            this.location = location;
            this.hidden = hidden;
        }

        public ILocation GetLocation()
        {
            return this.location;
        }

        public EntityType Type => type;

        public char DisplayLetter => displayLetter;

        public bool Hidden
        {
            get => hidden;
            set => hidden = value;
        }
    }
}