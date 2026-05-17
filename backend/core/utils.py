from datetime import datetime, timezone


def as_utc(value: datetime) -> datetime:
    """Normalize a datetime to UTC, assuming naive datetimes are already UTC."""
    if value.tzinfo is None or value.utcoffset() is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
