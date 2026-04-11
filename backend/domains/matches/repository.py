from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domains.matches.model import Match
from enums import MatchStatus


class MatchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_many(self, matches: list[Match]) -> list[Match]:
        """Persist multiple matches in a single flush. Does not commit."""
        for match in matches:
            self.session.add(match)
        await self.session.flush()
        for match in matches:
            await self.session.refresh(match)
        return matches

    async def exists_for_announcement(self, announcement_id: int) -> bool:
        """Return True if any matches exist for the given announcement."""
        result = await self.session.execute(
            select(Match.id).where(Match.announcement_id == announcement_id).limit(1)
        )
        return result.scalar() is not None

    async def has_unfinished_non_bye_matches(self, announcement_id: int) -> bool:
        """Return True if any non-BYE match is not COMPLETED."""
        result = await self.session.execute(
            select(Match.id)
            .where(
                Match.announcement_id == announcement_id,
                Match.is_bye.is_(False),
                Match.status != MatchStatus.COMPLETED,
            )
            .limit(1)
        )
        return result.scalar() is not None

    async def find_third_place_match(self, announcement_id: int) -> Match | None:
        """Fetch the third-place match for an announcement, if one exists."""
        result = await self.session.execute(
            select(Match).where(
                Match.announcement_id == announcement_id,
                Match.is_third_place.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def find_by_id(self, match_id: int) -> Match | None:
        """Fetch a single match by ID for write-side workflows."""
        result = await self.session.execute(select(Match).where(Match.id == match_id))
        return result.scalar_one_or_none()
