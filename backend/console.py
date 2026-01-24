#!/usr/bin/env python3
"""
Simple database console for GameAnnouncer project
Usage: python console.py or make console
"""

import asyncio
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent))

from core.config import get_settings
from core.db.container import create_db
from sqlalchemy import select


db = create_db()
settings = get_settings()


async def main():
    """Simple database console"""

    session = await db.get_session()

    print(f"✅ Connected to database: {settings.db.database}")
    print("⚙️  Database session available as 'session'")
    print("🔧 Settings available as 'settings'")
    print("⚙️  Database session available as 'session'")
    print("🔧 Settings available as 'settings'")
    print("\n💡 Import what you need:")
    print("  from models.game import Game")
    print("  from models.announcement import Announcement")
    print("  from api.v1.crud.game import game_crud")
    print("  result = await session.execute(select(Game))")
    print("  games = result.scalars().all()")
    print("\n📚 Use 'await' for async operations!")
    print("🔍 Type 'help()' for Python help\n")

    locals_dict = {
        "session": session,
        "db": db,
        "settings": settings,
        "select": select,
        "asyncio": asyncio,
    }

    try:
        import IPython
        import nest_asyncio

        nest_asyncio.apply()

        IPython.start_ipython(argv=[], user_ns=locals_dict)
    except ImportError:
        import code

        code.interact(local=locals_dict)
    finally:
        await db.dispose()
        print("❌ Database session closed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
