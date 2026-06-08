from __future__ import annotations

from fastapi import WebSocket


class ConnectionManager:
    """Manage WebSocket connections per user."""

    def __init__(self):
        self._connections: dict[int, WebSocket] = {}

    async def connect(self, ws: WebSocket, user_id: int):
        await ws.accept()
        self._connections[user_id] = ws

    def disconnect(self, user_id: int):
        self._connections.pop(user_id, None)

    async def send_to_user(self, user_id: int, data: dict):
        ws = self._connections.get(user_id)
        if ws:
            try:
                await ws.send_json(data)
            except Exception:
                self.disconnect(user_id)

    def is_connected(self, user_id: int) -> bool:
        return user_id in self._connections
