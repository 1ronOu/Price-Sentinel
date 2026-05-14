import factory

from app.models.item_models import Item
from tests.factories.coin_factory import CoinFactory
from tests.factories.user_factorie import UserFactory


class ItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Item
        sqlalchemy_session_persistence = None

    user = factory.SubFactory(UserFactory)
    coin = factory.SubFactory(CoinFactory)


    # target_price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    target_price = 100000
    currency = 'usd'
    is_notified = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return model_class(*args, **kwargs)
