from dataclasses import dataclass
from typing import Optional, Tuple

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
    latency: float = float('inf')

    def __str__(self) -> str:
        return f"{self.name} ({self.sponsor}) - {self.country}"

    @property
    def host_port(self) -> Tuple[str, int]:
        """Return host and port as tuple"""
        if ':' in self.host:
            host, port = self.host.split(':')
            return host, int(port)
        return self.host, 80