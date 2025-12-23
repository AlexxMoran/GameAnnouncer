import factory
from faker import Faker

fake = Faker()


class UserDictFactory(factory.Factory):
    class Meta:
        model = dict

    email = factory.LazyFunction(lambda: fake.unique.email())
    password = factory.Sequence(lambda n: f"pass{n}word")
    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    nickname = factory.LazyFunction(lambda: fake.user_name())
