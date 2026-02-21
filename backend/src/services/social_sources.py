# src/services/social_sources.py
from typing import List, Optional, TypedDict
from datetime import datetime


class SocialPost(TypedDict):
    platform: str        # "tiktok" | "instagram" | "youtube"
    topic: str
    post_id: str
    likes: int
    comments: int
    views: int
    posted_at: datetime
    collected_at: datetime


class SocialSource:
    def fetch_posts(
        self,
        topics: List[str],
        since_ts: Optional[datetime] = None,
    ) -> List[SocialPost]:
        raise NotImplementedError
