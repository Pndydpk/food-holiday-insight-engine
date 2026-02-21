# src/schemas/social_signal_schema.py

from pydantic import BaseModel
from typing import List, Optional, Dict

class SocialSignal(BaseModel):
    platform: str               # tiktok / instagram / x / youtube
    post_id: str
    timestamp: str             # ISO string for now
    text: Optional[str] = None
    hashtags: List[str] = []
    food_entities: List[str]   # extracted food items like ["ramen", "boba"]
    engagement: Dict[str, int] # {"likes": 1200, "comments": 34, "shares": 10}
    creator_followers: int
    geo: Optional[str] = None  # "US", "CA"
