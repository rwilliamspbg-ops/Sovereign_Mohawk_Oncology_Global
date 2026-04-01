import json
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Dict, List


class WebhookSiemForwarder:
    def __init__(self, endpoint: str | None = None, timeout_seconds: int = 2) -> None:
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds

    def forward(self, record: Dict[str, object]) -> None:
        if not self.endpoint:
            return
        body = json.dumps(record).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout_seconds):
            pass


class StrikePatternAlerter:
    def __init__(self, threshold: int = 3, window_minutes: int = 15) -> None:
        self.threshold = threshold
        self.window_minutes = window_minutes
        self._events: Dict[str, List[datetime]] = defaultdict(list)

    def record(self, client_id: str) -> bool:
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(minutes=self.window_minutes)
        self._events[client_id] = [ts for ts in self._events[client_id] if ts >= cutoff]
        self._events[client_id].append(now)
        return len(self._events[client_id]) >= self.threshold
