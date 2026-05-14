import factory

from app.models.item_models import Coin


class CoinFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Coin
        sqlalchemy_session_persistence = None

    api_id = 'bitcoin'
    title = 'Bitcoin'
    description = 'Bitcoin description'
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return model_class(*args, **kwargs)
