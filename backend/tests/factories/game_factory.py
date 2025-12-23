import factory
from faker import Faker
from typing import Any
from datetime import datetime, timezone

fake = Faker()

CATEGORIES = [
    "RTS",
    "TBS",
    "MOBA",
    "FPS",
    "TPS",
    "Fighting",
    "Racing",
    "Sports",
    "Card",
    "Battle Royale",
    "Rhythm",
    "Party",
    "Simulation",
]


class GameDictFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyFunction(lambda: fake.word())
    description = factory.LazyFunction(lambda: fake.sentence())
    category = factory.LazyFunction(lambda: fake.random_element(elements=CATEGORIES))
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())
    image_url = None
    announcements_count = 0


async def create_game_via_crud(crud, **overrides) -> Any:
    data = GameDictFactory(**overrides)
    return data
