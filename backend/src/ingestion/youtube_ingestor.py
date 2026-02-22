from typing import List
from src.ingestion.base_ingestor import BaseIngestor
from src.models.social_signal import SocialSignal

class YouTubeIngestor(BaseIngestor):
    platform = "youtube"

    def fetch_recent_signals(self, keyword: str) -> List[SocialSignal]:
        # TODO: Implement real YouTube API call in Step 4
        return []