namespace RatventureCore.Api
{
    public interface IGameFactory
    {
        IGame New();

        IGame Load();

        bool Save(IGame game);
    }
}
