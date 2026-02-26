from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from domains.matches.model import Match


class MatchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(self, match_id: int) -> Match | None:
        """Fetch a single match by ID."""
        result = await self.session.execute(select(Match).where(Match.id == match_id))
        return result.scalar_one_or_none()

    async def find_all_by_announcement_id(
        self, announcement_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[Match], int]:
        """Fetch paginated matches for an announcement ordered by round and match number."""
        count_result = await self.session.execute(
            select(func.count())
            .select_from(Match)
            .where(Match.announcement_id == announcement_id)
        )
        total = count_result.scalar_one()

        data_result = await self.session.execute(
            select(Match)
            .where(Match.announcement_id == announcement_id)
            .order_by(Match.round_number, Match.match_number)
            .offset(skip)
            .limit(limit)
        )
        return list(data_result.scalars().all()), total

    async def save(self, match: Match) -> Match:
        """Persist a match. Flushes but does not commit."""
        self.session.add(match)
        await self.session.flush()
        await self.session.refresh(match)
        return match

    async def save_many(self, matches: list[Match]) -> list[Match]:
        """Persist multiple matches in a single flush. Does not commit."""
        for match in matches:
            self.session.add(match)
        await self.session.flush()
        for match in matches:
            await self.session.refresh(match)
        return matches

    async def delete(self, match: Match) -> None:
        """Delete a match. Flushes but does not commit."""
        await self.session.delete(match)
        await self.session.flush()
