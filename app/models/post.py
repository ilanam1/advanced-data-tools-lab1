from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class Post:
    source: str
    collection_method: str
    topic: str
    title: str
    text: str
    author: Optional[str]
    created_at: Optional[str]
    url: Optional[str]
    extra: Dict[str, Any]

    def to_dict(self):
        return asdict(self)