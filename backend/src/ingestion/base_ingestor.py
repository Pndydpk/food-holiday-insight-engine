from abc import ABC, abstractmethod
from typing import List
from src.models.social_signal import SocialSignal

class BaseIngestor(ABC):
    platform: str

    @abstractmethod
    def fetch_recent_signals(self, keyword: str) -> List[SocialSignal]:
        """
        Fetch recent social signals for a given keyword.
        Must return a list of SocialSignal objects.
        """
        pass