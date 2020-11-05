namespace RatventureCore.Api
{
    public interface ILivingEntity : IEntity
    {
        int DealDamageTo(ILivingEntity enemy);

        bool CanDealDamageTo(ILivingEntity enemy);

        bool IsDead();

        IStats GetStats();
    }
}
