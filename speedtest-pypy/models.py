from dataclasses import dataclass
from typing import Optional

@dataclass
class ServerInfo:
    """Server information class for SpeedTest++"""
    id: int
    url: str
    lat: float
    lon: float
    name: str
    country: str
    sponsor: str
    host: str
    distance: float = 0.0
    latency: float = 0.0

    def __str__(self) -> str:
        return f"{self.name} ({self.sponsor}) - {self.country}"