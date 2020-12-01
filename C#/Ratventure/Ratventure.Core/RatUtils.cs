using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

namespace Ratventure.Core
{
    class RatUtils
    {
        private static readonly Random RandomGenerator = new Random();
        private static readonly BinaryFormatter Formatter = new BinaryFormatter();

        public static object LoadFile(string filePath)
        {
            try
            {
                using FileStream saveFile = new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.None);
                return Formatter.Deserialize(saveFile);
            }
            catch (Exception)
            {
                // ignored
            }

            return null;
        }

        public static bool SaveFile(string filePath, object item)
        {
            try
            {
                using Stream saveFile = new FileStream(filePath, FileMode.Create, FileAccess.Write);
                Formatter.Serialize(saveFile, item);
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
                return false;
            }

            return true;
        }

        public static int RandomNumber(int min, int max)
        {
            return RandomGenerator.Next(min, max);
        }
    }
}