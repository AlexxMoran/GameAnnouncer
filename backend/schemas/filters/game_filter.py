from typing import Optional
from .base_filter import BaseFilter


class GameFilter(BaseFilter):
    category: Optional[str] = None
