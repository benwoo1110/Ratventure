namespace RatventureCore.Api
{
    public interface ILivingEntity : IEntity
    {
        IStats Stats { get; }
        int DealDamageTo(ILivingEntity enemy);

        bool CanDealDamageTo(ILivingEntity enemy);

        bool IsDead();
    }
}
