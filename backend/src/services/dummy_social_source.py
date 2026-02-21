# src/services/dummy_social_source.py
import random
from datetime import datetime, timedelta
from typing import List, Optional

from services.social_sources import SocialSource, SocialPost


class DummySocialSource(SocialSource):
    def fetch_posts(
        self,
        topics: List[str],
        since_ts: Optional[datetime] = None,
    ) -> List[SocialPost]:
        posts: List[SocialPost] = []
        platforms = ["tiktok", "youtube"]  # MVP platforms

        now = datetime.utcnow()

        for topic in topics:
            for platform in platforms:
                num_posts = random.randint(5, 15)

                for i in range(num_posts):
                    posted_at = now - timedelta(hours=random.randint(1, 48))

                    post: SocialPost = {
                        "platform": platform,
                        "topic": topic,
                        "post_id": f"{platform}_{topic}_{i}_{int(posted_at.timestamp())}",
                        "likes": random.randint(50, 5000),
                        "comments": random.randint(5, 500),
                        "views": random.randint(1000, 50000),
                        "posted_at": posted_at,
                        "collected_at": now,
                    }

                    posts.append(post)

        return posts
