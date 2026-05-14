from pydantic import BaseModel, field_validator


class BaseFilter(BaseModel):
    """
    Base filter schema with common filtering attributes.
    """

    def values(self) -> dict:
        return self.model_dump(exclude_none=True)

    @field_validator("q", check_fields=False)
    @classmethod
    def validate_search_query(cls, v: str | None) -> str | None:
        """Validate search query: trim whitespace and return None for empty strings."""
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        return v
