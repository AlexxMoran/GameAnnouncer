from typing import Literal

from pydantic import BaseModel


class MatchResultUpdate(BaseModel):
    """Request body for reporting a match result - organizer picks the winner."""

    winner: Literal["participant1", "participant2"]
