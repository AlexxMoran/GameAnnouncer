import factory
from faker import Faker
from datetime import datetime
from enums import AnnouncementFormat, SeedMethod

fake = Faker()


class AnnouncementDictFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    content = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    game_id = factory.Sequence(lambda n: 100 + n)
    created_at = factory.LazyFunction(lambda: datetime.now().isoformat())
    updated_at = factory.LazyFunction(lambda: datetime.now().isoformat())
    image_url = None
    organizer_id = factory.Sequence(lambda n: n + 1)
    start_at = factory.LazyFunction(lambda: datetime(2026, 6, 1, 12, 0, 0).isoformat())
    registration_start_at = factory.LazyFunction(
        lambda: datetime(2026, 5, 1, 0, 0, 0).isoformat()
    )
    registration_end_at = factory.LazyFunction(
        lambda: datetime(2026, 5, 31, 23, 59, 59).isoformat()
    )
    is_registration_open = False
    max_participants = 10
    status = "pre_registration"
    format = AnnouncementFormat.SINGLE_ELIMINATION
    has_qualification = False
    seed_method = SeedMethod.RANDOM
    bracket_size = None
    third_place_match = True
    qualification_finished = False
    participants = factory.LazyFunction(list)
