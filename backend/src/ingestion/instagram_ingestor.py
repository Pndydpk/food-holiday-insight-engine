from typing import List
from src.ingestion.base_ingestor import BaseIngestor
from src.models.social_signal import SocialSignal

class InstagramIngestor(BaseIngestor):
    platform = "instagram"

    def fetch_recent_signals(self, keyword: str) -> List[SocialSignal]:
        # TODO: Implement real Instagram ingestion later
        return []