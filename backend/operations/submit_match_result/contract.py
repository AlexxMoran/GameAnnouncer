from typing import Literal

from pydantic import BaseModel


class SubmitMatchResultContract(BaseModel):
    """Contract for submitting a match result."""

    match_id: int
    winner: Literal["participant1", "participant2"]
