from typing import Optional
from models.announcement import Announcement
from schemas.registration_request import RegistrationRequestCreate
from enums.registration_status import RegistrationStatus
from models.registration_request import RegistrationRequest
from models.user import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from core.policies.authorize_action import authorize_action


class RegistrationRequestCRUD:
    async def get_all_by_user_id(
        self,
        session: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 10,
    ) -> list[RegistrationRequest]:
        result = await session.execute(
            select(RegistrationRequest)
            .where(RegistrationRequest.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(RegistrationRequest.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all_by_announcement_id(
        self,
        session: AsyncSession,
        announcement_id: int,
        skip: int = 0,
        limit: int = 10,
    ) -> list[RegistrationRequest]:
        result = await session.execute(
            select(RegistrationRequest)
            .where(RegistrationRequest.announcement_id == announcement_id)
            .offset(skip)
            .limit(limit)
            .order_by(RegistrationRequest.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(
        self,
        session: AsyncSession,
        registration_request_id: int,
        user: Optional[User] = None,
        action: Optional[str] = None,
    ) -> Optional[RegistrationRequest]:
        result = await session.execute(
            select(RegistrationRequest)
            .options(
                selectinload(RegistrationRequest.announcement).selectinload(
                    Announcement.participants
                ),
                selectinload(RegistrationRequest.announcement),
            )
            .where(RegistrationRequest.id == registration_request_id)
        )

        registration_request = result.scalar_one_or_none()

        if registration_request and user and action:
            authorize_action(user, registration_request, action)

        return registration_request

    async def get_by_user_and_announcement(
        self,
        session: AsyncSession,
        user_id: int,
        announcement_id: int,
    ) -> Optional[RegistrationRequest]:
        result = await session.execute(
            select(RegistrationRequest).where(
                RegistrationRequest.user_id == user_id,
                RegistrationRequest.announcement_id == announcement_id,
                RegistrationRequest.status.in_(
                    [RegistrationStatus.PENDING, RegistrationStatus.APPROVED]
                ),
            )
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        session: AsyncSession,
        registration_request_in: RegistrationRequestCreate,
        user: User,
    ) -> RegistrationRequest:
        registration_request = RegistrationRequest(
            **registration_request_in.model_dump()
        )
        registration_request.user = user
        session.add(registration_request)
        await session.commit()
        await session.refresh(registration_request)

        return registration_request

    async def _update_status(
        self,
        session: AsyncSession,
        registration_request: RegistrationRequest,
        status: RegistrationStatus,
    ) -> RegistrationRequest:
        registration_request.status = status

        if status == RegistrationStatus.APPROVED:
            announcement = registration_request.announcement
            if registration_request.user not in announcement.participants:
                announcement.participants.append(registration_request.user)

        await session.commit()
        await session.refresh(registration_request)

        return registration_request

    async def approve(
        self,
        session: AsyncSession,
        registration_request: RegistrationRequest,
        user: User,
    ) -> RegistrationRequest:
        authorize_action(user, registration_request, "approve")

        return await self._update_status(
            session=session,
            registration_request=registration_request,
            status=RegistrationStatus.APPROVED,
        )

    async def reject(
        self,
        session: AsyncSession,
        registration_request: RegistrationRequest,
        user: User,
    ) -> RegistrationRequest:
        authorize_action(user, registration_request, "reject")

        return await self._update_status(
            session=session,
            registration_request=registration_request,
            status=RegistrationStatus.REJECTED,
        )

    async def cancel(
        self,
        session: AsyncSession,
        registration_request: RegistrationRequest,
        user: User,
    ) -> RegistrationRequest:
        authorize_action(user, registration_request, "cancel")

        return await self._update_status(
            session=session,
            registration_request=registration_request,
            status=RegistrationStatus.CANCELLED,
        )


registration_request_crud = RegistrationRequestCRUD()
