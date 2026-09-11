from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # This list will hold all active WebSocket connections
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Accept the incoming WebSocket connection
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # Remove the connection when the user closes the tab/app
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # Send the message to EVERY connected client
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # If a connection dropped unexpectedly, remove it
                self.disconnect(connection)

# Create a single, global instance of the manager
manager = ConnectionManager()