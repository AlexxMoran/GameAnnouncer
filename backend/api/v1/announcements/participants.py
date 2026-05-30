from fastapi import APIRouter, Depends

from core.deps import SessionDep
from core.permissions import authorize_action
from core.schemas.base import DataResponse, PaginatedResponse
from core.users import current_user
from modules.announcements.model import Announcement
from modules.participants.queries import ParticipantQueries
from modules.participants.schemas.mutations import AnnouncementParticipantScoreUpdate
from modules.participants.schemas.responses import AnnouncementParticipantResponse
from modules.participants.services.update_score import update_participant_score
from modules.users.model import User

from .dependencies import get_announcement_dependency

router = APIRouter()


@router.get(
    "/{announcement_id}/participants",
    response_model=PaginatedResponse[AnnouncementParticipantResponse],
)
async def get_announcement_participants(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    announcement: Announcement = Depends(get_announcement_dependency),
) -> PaginatedResponse[AnnouncementParticipantResponse]:
    queries = ParticipantQueries(session)
    participants, total = await queries.find_all_by_announcement_id(
        announcement_id=announcement.id, skip=skip, limit=limit
    )
    return PaginatedResponse(
        data=participants,
        skip=skip,
        limit=limit,
        filtered_count=total,
        total_count=total,
    )


@router.patch(
    "/{announcement_id}/participants/{participant_id}",
    response_model=DataResponse[AnnouncementParticipantResponse],
)
async def patch_participant_score(
    session: SessionDep,
    participant_id: int,
    score_in: AnnouncementParticipantScoreUpdate,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementParticipantResponse]:
    authorize_action(user, announcement, "edit")
    participant = await update_participant_score(
        participant_id=participant_id,
        qualification_score=score_in.qualification_score,
        announcement=announcement,
        session=session,
    )
    await session.commit()
    return DataResponse(data=participant)
