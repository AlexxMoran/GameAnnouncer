from pydantic import BaseModel, ConfigDict

from enums import MatchStatus


class ParticipantBriefResponse(BaseModel):
    """Brief participant info embedded in a match response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    seed: int | None


class MatchResponse(BaseModel):
    """Single match in a bracket."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    round_number: int
    match_number: int
    participant1: ParticipantBriefResponse | None
    participant2: ParticipantBriefResponse | None
    winner_id: int | None
    status: MatchStatus
    is_bye: bool
    is_third_place: bool
    next_match_winner_id: int | None


class BracketResponse(BaseModel):
    """Full bracket for an announcement, grouped by round."""

    bracket_size: int
    rounds: dict[int, list[MatchResponse]]
