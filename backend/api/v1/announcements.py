from fastapi import APIRouter, UploadFile, File, Depends, Query

from exceptions import AppException
from domains.users.model import User
from core.services.avatar_uploader import upload_avatar
from core.schemas.base import PaginatedResponse, DataResponse
from domains.registration.schemas import (
    RegistrationRequestResponse,
    RegistrationFormCreate,
    RegistrationFormResponse,
)
from domains.registration.services.upsert_form import UpsertRegistrationFormService
from core.deps import SessionDep
from core.users import current_user, current_user_or_none
from core.permissions import authorize_action, get_permissions, get_batch_permissions

from domains.announcements.model import Announcement
from domains.announcements.repository import AnnouncementRepository
from domains.announcements.search import AnnouncementSearch
from domains.announcements.schemas import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementUpdate,
    AnnouncementFilter,
)
from domains.participants.repository import ParticipantRepository
from domains.participants.schemas import (
    AnnouncementParticipantResponse,
    AnnouncementParticipantScoreUpdate,
)
from domains.participants.services.update_score import update_participant_score
from domains.announcements.services.create import CreateAnnouncementService
from domains.announcements.services.lifecycle import AnnouncementLifecycleService
from domains.announcements.services.finalize_qualification import (
    FinalizeQualificationService,
)
from domains.announcements.services.generate_bracket import GenerateBracketService
from domains.announcements.utils.bracket import get_bracket
from domains.matches.repository import MatchRepository
from domains.matches.schemas import BracketResponse, MatchResponse

from domains.registration.repository import RegistrationRequestRepository

router = APIRouter(prefix="/announcements", tags=["announcements"])


async def get_announcement_dependency(
    session: SessionDep,
    announcement_id: int,
) -> Announcement:
    repo = AnnouncementRepository(session)
    announcement = await repo.find_by_id(announcement_id)
    if not announcement:
        raise AppException("Announcement not found", status_code=404)
    return announcement


@router.get("", response_model=PaginatedResponse[AnnouncementResponse])
async def get_announcements(
    session: SessionDep,
    filters: AnnouncementFilter = Depends(),
    user: User | None = Depends(current_user_or_none),
    skip: int = 0,
    limit: int = 10,
) -> PaginatedResponse[AnnouncementResponse]:
    search = AnnouncementSearch(session=session, filters=filters)
    announcements = await search.results(skip=skip, limit=limit)
    announcements_count = await search.count()
    get_batch_permissions(user, announcements)
    return PaginatedResponse(
        data=announcements, skip=skip, limit=limit, total=announcements_count
    )


@router.get("/{announcement_id}", response_model=DataResponse[AnnouncementResponse])
async def get_announcement(
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User | None = Depends(current_user_or_none),
) -> DataResponse[AnnouncementResponse]:
    announcement.permissions = get_permissions(user, announcement)
    return DataResponse(data=announcement)


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
    repo = ParticipantRepository(session)
    participants, total = await repo.find_all_by_announcement_id(
        announcement_id=announcement.id, skip=skip, limit=limit
    )
    return PaginatedResponse(data=participants, skip=skip, limit=limit, total=total)


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


@router.get(
    "/{announcement_id}/registration_requests",
    response_model=PaginatedResponse[RegistrationRequestResponse],
)
async def get_announcement_registration_requests(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> PaginatedResponse[RegistrationRequestResponse]:
    """
    List all registration requests for an announcement.

    Restricted to the announcement organizer and admins.
    Returns 401 if unauthenticated, 403 if authenticated but unauthorized.
    """
    authorize_action(user, announcement, "edit")
    repo = RegistrationRequestRepository(session)
    registration_requests, total = await repo.find_all_by_announcement_id(
        announcement_id=announcement.id, skip=skip, limit=limit
    )
    return PaginatedResponse(
        data=registration_requests, skip=skip, limit=limit, total=total
    )


@router.post("", response_model=DataResponse[AnnouncementResponse], status_code=201)
async def create_announcement(
    session: SessionDep,
    announcement_in: AnnouncementCreate,
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, Announcement, "create")
    service = CreateAnnouncementService(
        session=session, announcement_in=announcement_in, user=user
    )
    announcement = await service.call()
    await session.commit()
    return DataResponse(data=announcement)


@router.patch("/{announcement_id}", response_model=DataResponse[AnnouncementResponse])
async def update_announcement(
    session: SessionDep,
    announcement_in: AnnouncementUpdate,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "edit")
    repo = AnnouncementRepository(session)
    for field, value in announcement_in.model_dump(exclude_unset=True).items():
        setattr(announcement, field, value)
    announcement = await repo.save(announcement)
    await session.commit()
    return DataResponse(data=announcement)


@router.delete("/{announcement_id}", response_model=DataResponse[str])
async def delete_announcement(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[str]:
    authorize_action(user, announcement, "delete")
    repo = AnnouncementRepository(session)
    await repo.delete(announcement)
    await session.commit()
    return DataResponse(data="Announcement deleted successfully")


@router.post(
    "/{announcement_id}/start_qualification",
    response_model=DataResponse[AnnouncementResponse],
)
async def start_qualification(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "manage_lifecycle")
    service = AnnouncementLifecycleService(announcement, session)
    announcement = await service.start_qualification()
    await session.commit()
    return DataResponse(data=announcement)


@router.post(
    "/{announcement_id}/finalize_qualification",
    response_model=DataResponse[AnnouncementResponse],
)
async def finalize_qualification(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "manage_lifecycle")
    service = FinalizeQualificationService(announcement, session)
    announcement = await service.call()
    await session.commit()
    return DataResponse(data=announcement)


@router.post(
    "/{announcement_id}/generate_bracket",
    response_model=DataResponse[AnnouncementResponse],
)
async def generate_bracket(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "manage_lifecycle")
    service = GenerateBracketService(announcement, session)
    announcement = await service.call()
    await session.commit()
    return DataResponse(data=announcement)


@router.get(
    "/{announcement_id}/matches",
    response_model=PaginatedResponse[MatchResponse],
)
async def get_announcement_matches(
    session: SessionDep,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    announcement: Announcement = Depends(get_announcement_dependency),
) -> PaginatedResponse[MatchResponse]:
    repo = MatchRepository(session)
    matches, total = await repo.find_all_by_announcement_id(
        announcement_id=announcement.id, skip=skip, limit=limit
    )
    return PaginatedResponse(data=matches, skip=skip, limit=limit, total=total)


@router.get(
    "/{announcement_id}/bracket",
    response_model=DataResponse[BracketResponse],
)
async def get_announcement_bracket(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
) -> DataResponse[BracketResponse]:
    data = await get_bracket(announcement, session)

    return DataResponse(data=data)


@router.post(
    "/{announcement_id}/cancel",
    response_model=DataResponse[AnnouncementResponse],
)
async def cancel_announcement(
    session: SessionDep,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "manage_lifecycle")
    service = AnnouncementLifecycleService(announcement, session)
    announcement = await service.cancel()
    await session.commit()
    return DataResponse(data=announcement)


@router.put(
    "/{announcement_id}/registration_form",
    response_model=DataResponse[RegistrationFormResponse],
)
async def upsert_registration_form(
    session: SessionDep,
    registration_form_in: RegistrationFormCreate,
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[RegistrationFormResponse]:
    authorize_action(user, announcement, "edit")
    service = UpsertRegistrationFormService(
        session=session,
        announcement=announcement,
        registration_form_in=registration_form_in,
    )
    registration_form = await service.call()
    await session.commit()
    await session.refresh(registration_form)
    return DataResponse(data=registration_form)


@router.post(
    "/{announcement_id}/upload_image", response_model=DataResponse[AnnouncementResponse]
)
async def upload_announcement_image(
    session: SessionDep,
    file: UploadFile = File(...),
    announcement: Announcement = Depends(get_announcement_dependency),
    user: User = Depends(current_user),
) -> DataResponse[AnnouncementResponse]:
    authorize_action(user, announcement, "edit")
    image_url = await upload_avatar(
        object_type="announcement", object_id=announcement.id, file=file
    )
    announcement.image_url = image_url
    repo = AnnouncementRepository(session)
    announcement = await repo.save(announcement)
    await session.commit()
    return DataResponse(data=announcement)
