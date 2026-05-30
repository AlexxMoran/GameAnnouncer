from fastapi import APIRouter, Depends

from core.schemas.base import DataResponse
from modules.matches.model import Match
from modules.matches.schemas.responses import MatchResponse

from .dependencies import get_match_dependency

router = APIRouter()


@router.get("/{match_id}", response_model=DataResponse[MatchResponse])
async def get_match(
    match: Match = Depends(get_match_dependency),
) -> DataResponse[MatchResponse]:
    return DataResponse(data=match)
