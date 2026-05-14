import factory

from app.models.user_models import User
from app.services.hash_service import hash_password


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = None

    name = factory.Faker("name")
    password = factory.Faker("password")
    telegram_id = factory.Faker("pyint")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = hash_password(kwargs.pop("password"))
        return model_class(*args, **kwargs)
