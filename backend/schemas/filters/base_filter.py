from pydantic import BaseModel


class BaseFilter(BaseModel):
    """
    Base filter schema with common filtering attributes.
    """

    def values(self) -> dict:
        return self.model_dump(exclude_none=True)
