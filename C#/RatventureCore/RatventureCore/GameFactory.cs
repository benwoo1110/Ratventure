using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using RatventureCore.Api;
using RatventureCore.GamePlay;

namespace RatventureCore
{
    public class GameFactory : IGameFactory
    {
        private static readonly string SaveFileName = @"save.bin";
        private static readonly BinaryFormatter Formatter = new BinaryFormatter();


        public IGame New()
        {
            return new Game();
        }

        public IGame Load()
        {
            try
            {
                using FileStream saveFile = new FileStream(SaveFileName, FileMode.Open, FileAccess.Read, FileShare.None);
                return (Game)Formatter.Deserialize(saveFile);
            }
            catch (Exception)
            {
                // ignored
            }

            return null;
        }

        public bool Save(IGame game)
        {
            try
            {
                using Stream saveFile = new FileStream(SaveFileName, FileMode.Create, FileAccess.Write);
                Formatter.Serialize(saveFile, game);
            }
            catch (Exception)
            {
                return false;
            }

            return true;
        }
    }
}
