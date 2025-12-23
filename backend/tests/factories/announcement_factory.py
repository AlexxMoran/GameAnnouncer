import factory
from faker import Faker
from datetime import datetime, timezone

fake = Faker()


class AnnouncementDictFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    content = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    game_id = factory.Sequence(lambda n: 100 + n)
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())
    image_url = None
    organizer_id = factory.Sequence(lambda n: n + 1)
