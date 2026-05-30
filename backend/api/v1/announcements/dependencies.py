from exceptions import AppException
from core.deps import SessionDep
from modules.announcements.model import Announcement
from modules.announcements.queries import AnnouncementQueries


async def get_announcement_dependency(
    session: SessionDep,
    announcement_id: int,
) -> Announcement:
    queries = AnnouncementQueries(session)
    announcement = await queries.find_by_id(announcement_id)
    if not announcement:
        raise AppException("Announcement not found", status_code=404)
    return announcement
