import factory
from faker import Faker
from datetime import datetime, timezone

fake = Faker()


class RegistrationRequestDictFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    announcement_id = factory.Sequence(lambda n: 200 + n)
    user_id = factory.Sequence(lambda n: n + 1)
    status = factory.LazyFunction(lambda: "pending")
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())
